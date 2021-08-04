import pymongo
import urllib.parse
from secrets import db_pw

# This project uses MongoDB

CONNECTION_STRING = "mongodb+srv://drew:" + urllib.parse.quote(db_pw) + "@cluster0.2ljw7.mongodb.net/retryWrites=true&w=majority"
DB_NAME = "td_bot"

def test_db_connection():
    '''
    Primarily for testing purposes. Connects to a MongoDB cluster
    :return:
    '''
    client = pymongo.MongoClient(CONNECTION_STRING)
    print("Current database names:")
    print(client.database_names())


def get_access_token():
    '''
    Fetches the most recent access_token (required for most API calls)
    :return: access_token (string)
    '''
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.td_bot
    return(db.access_tokens.find_one())


def insert_access_token(access_token_Json):
    '''
    Clears the access_tokens table and inserts a new access_token Json into the database
    :param access_token_Json: Includes access_token, expires_in, and time_created
    :return:
    '''
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.td_bot
    access_tokens = db.access_tokens
    access_tokens.remove()
    access_tokens.insert_one(access_token_Json)