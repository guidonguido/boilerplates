import logging
import os
import sys
from telethon import TelegramClient
from pdf2image import convert_from_path


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

def get_filepaths(
        directory_path: str,
):
    """
    Get all file paths from subdirectories in a directory
    :param directory_path:
    :return:
    """
    file_paths = []
    for root, directories, files in os.walk(directory_path):
        for directory in directories:
            logging.debug(f"Navigating download directory: {directory}")
            for filename in os.listdir(os.path.join(root, directory)):
                filepath = os.path.join(root, directory, filename)
                if os.path.isfile(filepath) and filename.endswith(".pdf") and not filename.endswith(".part"):
                    logging.info(f"Found uploadable file: {filepath}")
                    file_paths.append(filepath)
                else:
                    logging.debug(f"Skipping not-uploadable file: {filepath}")
    return file_paths

def delete_parent_folder(
        filepath: str,
        downloads_path: str,
):
    """
    Delete folder containing file
    :param filepath:
    :return:
    """
    logging.info(f"Deleting parent folder for file: {filepath}")
    
    parent_folder = os.path.dirname(filepath)

    if parent_folder != downloads_path:
        for root, dirs, files in os.walk(parent_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(parent_folder)
        logging.info(f"Deleted parent folder for file: {filepath}")
        
async def upload_file(
    client,
    channel_id: int,
    filepath: str,
) -> bool:
    await client.send_file(channel_id, filepath)
    return True

def delete_old_directories(
        directory_path: str,
        days: int,
):
    ## TODO: Implement this
    return True

def generate_firstpage_image(filepath):
    try:
        images = convert_from_path(filepath, last_page=1, first_page=0)
        image_filepath = filepath + ".jpg"
        images[0].save(image_filepath, "JPEG")
        return image_filepath
    except Exception as e:
        log_exception("Error generating first page image", sys.exc_info())
        raise e
    
def delete_unwanted_files(
        directory_path: str,
):
    """
    Delete unwanted files
    :param directory_path:
    :return:
    """
    for root, directories, files in os.walk(directory_path):
        for directory in directories:
            logging.debug(f"Navigating download directory: {directory}")
            for filename in os.listdir(os.path.join(root, directory)):
                filepath = os.path.join(root, directory, filename)
                if os.path.isfile(filepath) and not filename.endswith(".pdf") and not filename.endswith(".part"):
                    logging.info(f"Found trash file: {filepath}")
                    delete_parent_folder(filepath, directory_path)
    return True
