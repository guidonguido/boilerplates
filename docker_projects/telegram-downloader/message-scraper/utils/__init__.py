import json
import sys
from telethon import TelegramClient
import logging
import os
import re

from utils.CrawlJob import CrawlJob

def log_exception(message: str, sys_exc_info) -> None:
    exc_type, exc_obj, exc_tb = sys_exc_info
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logging.critical(f"{message}: [{exc_type} | {fname}@{exc_tb.tb_lineno}] {exc_obj}")

async def set_telegram_client(
    api_id,
    api_hash,
    phone_number,
    session_path,
):
    # Create a Telegram client with the specified API ID, API hash and phone number
    client = TelegramClient(session_path, api_id, api_hash)
    await client.start()
    logging.info(f"Telegram client session started with phone number '{phone_number}'")

    # Check if the user is already authorized, otherwise prompt the user to authorize the client
    if not await client.is_user_authorized():
        logging.info(f"User '{phone_number}' is not authorized. Sending code request...")
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Enter the code: '))
    
    return client

async def get_messages_from_time(
    client,
    channel_id,
    start_time,
):
    messages = []

    # Get messages from the specified channel
    async for message in client.iter_messages(channel_id, reverse=True, offset_date=start_time):
        logging.info(f"Read message '{message.text}' sent at '{message.date}' ")
        messages.append(message)

    return messages

async def get_messages_after_id(
    client,
    channel_id,
    min_id,
):
    messages = []

    # Get messages from the specified channel
    async for message in client.iter_messages(channel_id, reverse = True, min_id=min_id, limit=20):
        logging.info(f"Read message '{message.text}' sent at '{message.date}' ")
        messages.append(message)

    return messages

def extract_url_description_tuples(
        domain,
        message,
        description_exclusion = None,
):
    # Define a regular expression pattern to match the URL
    pattern = re.compile(rf'\[url=(https?://{domain}[^\]]+)\]([^[]+)....\[/url\]')
    pattern_detailed = re.compile(rf'\[url=(https?://{domain}[^\]]+)\]_\[.*\] ?([^\[]+)....\[/url\]')

    # Use the findall method to extract all matches
    matches = pattern.findall(message)
    matches += pattern_detailed.findall(message)

    # Create tuples with URL and description
    result_tuples = []
    for url, description in matches:
        # If there is a description exclusion, check if the description contains any of the exclusion words
        if description_exclusion:
            if not any(exclusion in description for exclusion in description_exclusion):
                result_tuples.append((url, description))
        else:
            result_tuples.append((url, description))

    # If there are matches, print the first one (assuming there is only one URL in the message)
    if result_tuples:
        logging.info("Extracted URLs:", result_tuples)
        return result_tuples
    else:
        logging.info("No URL found in the message.")
        return []

def save_crawl_job(
    crawl_job,
    path,
):
    # Save the crawl job to a file
    with open(path, 'w', encoding='utf-8') as outfile:
        outfile.write("[")
        json.dump(crawl_job.__dict__, outfile, ensure_ascii=False, indent=4)
        outfile.write("]")

    logging.info(f"Crawl job saved to '{path}'")

def clean_folder(
    path,
):
    # Clean the folder
    for filename in os.listdir(path):
        
        file_path = os.path.join(path, filename)
        
        if os.path.isfile(file_path):
            os.unlink(file_path)
