# Microservice to read telegram messages and send them to kafka
import asyncio
from datetime import datetime, timedelta
import logging
import os
import sys
import time
import cfg_load

from utils import (
    CrawlJob,
    set_telegram_client,
    get_messages_after_id,
    get_messages_from_time,
    log_exception,
    extract_url_description_tuples,
    save_crawl_job,
    clean_folder,
)

from utils.sqlite import (
    create_connection,
    create_table,
    get_max_message_id,
    create_message_with_links,
)

from utils.entities.Message import Message
from utils.entities.Link import Link

#########################
# Environment variables #
#########################
config = cfg_load.load("/config/config.yaml")
api_id = config["telethon"]["api_id"]
api_hash = config["telethon"]["api_hash"]
phone_number = config["telethon"]["phone_number"]
start_interval = config["scraper"]["start_interval"] # seconds
# Get the ID of the specified channel
channel_id = config["telethon"]["channel_id"]
domain = config["scraper"]["domain"]
crawl_job_path = config["scraper"]["crawl_job_path"]
db_path = config["scraper"]["db_path"]
session_path = config["telethon"]["session_path"]  
exclusion_list = config["scraper"]["exclusion_list"]

# Setup logger
logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s')

def create_db_connection():
    # Create connection to database
    conn = create_connection(db_path)
    # Create tables
    create_table(conn, """ CREATE TABLE IF NOT EXISTS messages (
                                    id integer PRIMARY KEY,
                                    date text NOT NULL
                                ); """)
    create_table(conn, """ CREATE TABLE IF NOT EXISTS links (
                                    id integer PRIMARY KEY,
                                    url text NOT NULL,
                                    message_id integer NOT NULL,
                                    FOREIGN KEY (message_id) REFERENCES messages (id)
                                ); """)
    return conn

async def process_message(db_conn, message):
    try:
        db_message = Message(message.id, message.date)
        db_links = []

        # Extract url and description from message
        url_description_tuples = extract_url_description_tuples(domain, message.text, exclusion_list)


        for url_description_tuple in url_description_tuples:
            # Create crawl job object
            crawl_job = CrawlJob(
                            text = url_description_tuple[0],
                            packageName = url_description_tuple[1],
                            comment = f"Message sent at {message.date}"
                        )

            # Save crawl job to file
            save_crawl_job(
                crawl_job,
                crawl_job_path+"/"+url_description_tuple[1]+".crawljob"
            )

            # Create link object
            db_links.append(Link(None, url_description_tuple[0], message.id))
        
        # After saving the crawl job, save the message and links to the database
        create_message_with_links(db_conn, db_message, db_links)

    except Exception:
        log_exception(
            f"Error while processing message '{message.text}' sent at '{message.date}'",
            sys.exc_info(),
        )      

async def read_messages():
    logging.getLogger().info("Telegram reader started")
    try:
        # Create connection to database
        conn = create_db_connection()

        # Get max message id
        last_message_id = get_max_message_id(conn)

        # Set client object
        CLIENT = await set_telegram_client(api_id, api_hash, phone_number, session_path)

        try:
            if last_message_id == None:
                start_time = datetime.now() - timedelta(seconds=start_interval)
                messages = await get_messages_from_time(CLIENT, channel_id, start_time)
                if len(messages) > 0:
                    last_message_id = messages[-1].id

                    for message in messages:
                        await process_message(conn, message)   
                else:
                    messages = await get_messages_after_id(CLIENT, channel_id, 0)
                    last_message_id = messages[-1].id
        except Exception:
                log_exception(
                    f"Error while reading messages from telegram.",
                    sys.exc_info(),
                )  
        while True:

            try:
                # Wait (additional) 10 seconds before reading new messages
                time.sleep(10)
                
                try:
                    # Remove added crawl jobs from filesystem
                    clean_folder(os.path.join(crawl_job_path, "added"))
                except Exception:
                    log_exception(
                        f"Error while cleaning added crawl jobs folder.",
                        sys.exc_info(),
                    )

                # Get new messages from the specified channel
                messages = await get_messages_after_id(CLIENT, channel_id, last_message_id)

                if len(messages) > 0:
                    # Update last message id
                    last_message_id = messages[-1].id

                for message in messages:
                    await process_message(conn, message)

                # Wait 50 seconds before reading new messages
                time.sleep(50)

            except Exception:
                log_exception(
                    f"Error while reading messages from telegram.",
                    sys.exc_info(),
                )    
    finally:
        logging.info("Telegram reader stopped")
        
        # Close connection to database
        conn.close()

        # Disconnect telegram client
        await CLIENT.disconnect()

asyncio.run(read_messages())            
        