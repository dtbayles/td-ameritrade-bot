import pymongo
import urllib.parse
from secrets import CONNECTION_STRING


# This project uses MongoDB
def test_db_connection():
    """
    Primarily for testing purposes. Connects to a MongoDB cluster
    :return:
    """
    client = pymongo.MongoClient(CONNECTION_STRING)
    print("Current database names:")
    print(client.list_database_names())


def get_access_token():
    """
    Fetches the most recent access_token (required for most API calls)
    :return: access_token (string)
    """
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.td_bot
    return db.access_tokens.find_one()


def insert_access_token(access_token_json):
    """
    Clears the access_tokens table and inserts a new access_token Json into the database
    :param access_token_json: Includes access_token, expires_in, and time_created
    :return:
    """
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.td_bot
    access_tokens = db.access_tokens
    access_tokens.remove()
    access_tokens.insert_one(access_token_json)
