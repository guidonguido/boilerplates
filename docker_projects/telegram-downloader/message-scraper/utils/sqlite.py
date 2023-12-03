import logging
import sqlite3
from sqlite3 import Error
import sys

from utils import log_exception
from utils.entities import Message
from utils.entities.Link import Link


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info(f"Connection to database '{db_file}' successful")
        return conn
    except Error as e:
        log_exception(
            f"Error while creating connection to database.",
            sys.exc_info(),
        )
    return conn
    
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        logging.info(f"Creating table from statement '{create_table_sql}'")
        c = conn.cursor()
        c.execute(create_table_sql)
        logging.info(f"Table created")
    except Error as e:
        log_exception(
            f"Error while creating table.",
            sys.exc_info(),
        )

def create_message_with_links(conn, message: Message, links: list[Link]):
    """
    Create a new message with links
    :param conn:
    :param message:
    :param links:
    :return: message id
    """
    message_sql = ''' INSERT INTO messages(id, date)
              VALUES(?,?) '''
    
    link_sql = ''' INSERT INTO links(url, message_id)
                VALUES(?,?) '''
    
    cur = conn.cursor()

    # Insert message
    cur.execute(message_sql, message.to_tuple())
    message_id = cur.lastrowid
    
    # Insert links
    for link in links:
        link.message_id = message_id
        cur.execute(link_sql, link.to_tuple())
      
    # Commit changes
    conn.commit()

    logging.info(f"Message with id '{message_id}' created")
    
    return message_id
    
def get_max_message_id(conn):
    """
    Get max message id
    :param conn:
    :return: max message id
    """
    sql = ''' SELECT MAX(id) FROM messages '''
    
    cur = conn.cursor()
    cur.execute(sql)
    max_id = cur.fetchone()[0]
    
    return max_id