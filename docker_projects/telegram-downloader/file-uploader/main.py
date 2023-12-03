import asyncio
import logging
import sys
import time
import cfg_load
from utils import (
    log_exception,
    get_filepaths,
    delete_parent_folder,
    set_telegram_client,
    upload_file,
    generate_firstpage_image,
    delete_unwanted_files,
)

#########################
# Environment variables #
#########################
config = cfg_load.load("/config/config.yaml")
api_id = config["telethon"]["api_id"]
api_hash = config["telethon"]["api_hash"]
phone_number = config["telethon"]["phone_number"]
channel_id = config["telethon"]["channel_id"]
downloads_path = config["uploader"]["downloads_path"]  
session_path = config["telethon"]["session_path"]  

# Setup logger
logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(message)s')

async def start_uploader():
    """
    Upload files in downloads directory
    """

    logging.info("Uploader started")

    # Set client object
    CLIENT = await set_telegram_client(api_id, api_hash, phone_number, session_path)

    while True:
        try:
            # Sleep for 10 seconds before checking for new files
            time.sleep(10)

            logging.debug("\nChecking for new files to upload")
            file_paths = get_filepaths(downloads_path)

            if len(file_paths) == 0:
                delete_unwanted_files(downloads_path)
                logging.debug("No files to upload")

            for filepath in file_paths:

                try:   
                    #Generate first page image
                    image_path = generate_firstpage_image(filepath)
                    logging.info(f"Uploading file: {filepath}")
                    await upload_file(CLIENT, channel_id, image_path)
                    time.sleep(10)
                except Exception:
                    log_exception(f"Failed to upload or generate image file: {filepath} or {image_path}. Skipping this step.", sys.exc_info())

                try:
                    # Upload file
                    logging.info(f"Uploading file: {filepath}")
                    await upload_file(CLIENT, channel_id, filepath)
                    delete_parent_folder(filepath, downloads_path)
                except ConnectionError:
                    log_exception(f"Connection error while uploading file: {filepath}", sys.exc_info())
                    time.sleep(120)
                except Exception:
                    log_exception(f"Failed to upload file: {filepath}", sys.exc_info())

                # Sleep for 15 seconds before uploading next file
                time.sleep(40)
        except Exception:
            log_exception("Uploader failed", sys.exc_info())

asyncio.run(start_uploader())
