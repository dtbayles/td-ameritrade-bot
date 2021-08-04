import requests
import urllib.parse
import json
import pymongo
import td_api_requests
import database
from secrets import access_token, redirect_uri, client_id, refresh_token, db_pw

# ToDo create MongoDB schema (research and see if it is best practice)
def main():
    current_access_token = database.get_access_token()
    print(current_access_token)

    # new_access_token = td_api_requests.refresh_access_token()
    # database.insert_access_token(new_access_token)

    database.test_db_connection()


#Todo check if the access token is alive and request a new one, if not
def check_access_token_status():
    print("FixMe")

if __name__ == "__main__":
    main()