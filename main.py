import requests
import urllib.parse
import json
import pymongo
import td_api_requests
import time
from mongo import MongoDB
from assets.logger import Logger
from tdameritrade import TDAmeritrade
import database

# from secrets import access_token, redirect_uri, client_id, refresh_token, db_pw

'''
User has:
    Accounts
    deviceID
    ClientID
    Name
    
'''


class Main:

    def __init__(self):
        self.logger = Logger()
        self.mongo = MongoDB(self.logger)
        self.logger.mongo = self.mongo
        self.trading_account = object
        self.traders = {}
        self.accounts = []
        self.not_connected = []

    def initialize_accounts(self):
        """
        Fetches all accounts form the database
        :return:
        """
        # Fetch trading account from database

    def setupTraders(self):
        """ METHOD GETS ALL USERS ACCOUNTS FROM MONGO AND CREATES LIVE TRADER INSTANCES FOR THOSE ACCOUNTS.
            IF ACCOUNT INSTANCE ALREADY IN SELF.TRADERS DICT, THEN ACCOUNT INSTANCE WILL NOT BE CREATED AGAIN.
        """
        try:
            # GET ALL USERS ACCOUNTS

            users = self.mongo.users.find({})
            for user in users:
                for account_id, info in user["Accounts"].items():
                    if account_id not in self.traders and account_id not in self.not_connected:
                        tdameritrade = TDAmeritrade(self.mongo, user, account_id, self.logger)
                        connected = tdameritrade.initial_connect()
                        if connected:
                            # obj = LiveTrader(user, self.mongo, PushNotification(
                            #     user["deviceID"], self.logger, self.gmail), self.logger, account_id, info["Asset_Type"],
                            #                  tdameritrade)
                            # self.traders[account_id] = obj
                            time.sleep(0.1)
                        else:
                            self.not_connected.append(account_id)
                    self.accounts.append(account_id)
        except Exception:
            self.logger.ERROR()

    # ToDo create MongoDB schema (research and see if it is best practice)
    def run(self):
        print("deez")
        self.setupTraders()

        # current_access_token = database.get_access_token()
        # print(current_access_token)

        # new_access_token = td_api_requests.refresh_access_token()
        # database.insert_access_token(new_access_token)

        # database.test_db_connection()

    # Todo check if the access token is alive and request a new one, if not
    def check_access_token_status(self):
        print("FixMe")


if __name__ == "__main__":
    """
    START OF SCRIPT
    """

    main = Main()

    # while True:
    #     main.run()

    main.run()
