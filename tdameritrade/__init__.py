import urllib.parse
import requests
import time
import json
from datetime import datetime, timedelta
from secrets import redirect_uri, client_id, refresh_token, access_token


class TDAmeritrade:
    def __init__(self, mongo, user, account_id, logger):
        self.user = user
        self.account_id = account_id
        self.logger = logger
        self.users = mongo.users
        self.client_id = self.user["ClientID"]
        self.headers = {}
        self.terminate = False
        self.invalid_request_count = 0
        self.no_go_token_sent = False

    def generate_refresh_token(self):
        """
        How to generate a new refresh token if old one has completely expired (older than 90 days)
        :return:
        """
        auth_url = "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=" + urllib.parse.quote(
            redirect_uri) + "&client_id=" + urllib.parse.quote(client_id) + "%40AMER.OAUTHAP"
        print(auth_url)
        '''
        1. Sign in and then URL decode the code --> urllib.parse.unquote(CODE)
            print(urllib.parse.unquote(CODE))
        2. Enter the following request data online: https://developer.tdameritrade.com/authentication/apis/post/token-0
            reqData = {
                'grant_type': 'authorization_code',
                'access_type': 'offline',
                'code': urllib.parse.unquote("CODE"),
                'client_id': secrets.client_id,
                'redirect_uri': secrets.redirect_uri
            }
        3. Save the refresh_token and access_token
        '''

    #@exception_handler
    def initial_connect(self):
        """
        Initiates connection to TDAmeritrade by checking the access token validity, requestion a
        new one if necessary, and logging all progress
        :return: true if successful, false if error
        """
        self.logger.INFO(
            f"Connecting {self.user['Name']} to TDAmeritrade ({self.account_id})")
        is_valid = self.check_token_validity()
        if is_valid:
            self.logger.INFO(f"Connected {self.user['Name']} to TDAmeritrade ({self.account_id})")
            return True
        else:
            self.logger.CRITICAL(f"Failed to connect {self.user['Name']} to TDAmeritrade ({self.account_id})")
            return False

    #@exception_handler
    def check_token_validity(self):
        """
        Checks if current access token is valid
        :return: boolean; true if successful, false if error
        """
        # Get user data
        user = self.users.find_one({"Name": self.user["Name"]})

        # Add existing token to header
        self.headers.update({"Authorization": f"Bearer {user['Accounts'][self.account_id]['access_token']}"})

        # Check if access token needs to be updated
        age_sec = round(time.time() - user["Accounts"][self.account_id]["created_at"])
        if age_sec >= user["Accounts"][self.account_id]['expires_in'] - 60:
            token = self.getNewTokens(user["Accounts"][self.account_id])
            if token:
                # Add new token data to user data in database
                self.users.update_one({"Name": self.user["Name"]}, {
                    "$set": {f"Accounts.{self.account_id}.expires_in": token['expires_in'],
                             f"Accounts.{self.account_id}.access_token": token["access_token"],
                             f"Accounts.{self.account_id}.created_at": time.time()}})
                # Add new token to header
                self.headers.update({"Authorization": f"Bearer {token['access_token']}"})
            else:
                return False

        # Check if refresh token needs to be updated
        now = datetime.strptime(datetime.strftime(
            datetime.now().replace(microsecond=0), "%Y-%m-%d"), "%Y-%m-%d")
        refresh_exp = datetime.strptime(
            user["Accounts"][self.account_id]["refresh_exp_date"], "%Y-%m-%d")
        days_left = (refresh_exp - now).total_seconds() / 60 / 60 / 24
        if days_left == 1:
            token = self.getNewTokens(user["Accounts"][self.account_id], refresh_type="Refresh Token")
            if token:
                # ADD NEW TOKEN DATA TO USER DATA IN DB
                self.users.update_one({"Name": self.user["Name"]}, {
                    "$set": {f"{self.account_id}.refresh_token": token['refresh_token'],
                             f"{self.account_id}.refresh_exp_date": (datetime.now().replace(
                                 microsecond=0) + timedelta(days=90)).strftime("%Y-%m-%d")}})

                self.headers.update({"Authorization": f"Bearer {token['access_token']}"})
            else:
                return False

        return True

    #@exception_handler todo change name to refresh_tokens
    def getNewTokens(self, token, refresh_type="Access Token"):
        """ METHOD GETS NEW ACCESS TOKEN, OR NEW REFRESH TOKEN IF NEEDED.
        Args:
            token ([dict]): TOKEN DATA (ACCESS TOKEN, REFRESH TOKEN, EXP DATES)
            refresh_type (str, optional): CAN BE EITHER Access Token OR Refresh Token. Defaults to "Access Token".
        Raises:
            Exception: IF RESPONSE STATUS CODE IS NOT 200
        Returns:
            [json]: NEW TOKEN DATA
        """
        auth_url = 'https://api.tdameritrade.com/v1/oauth2/token'
        reqData = {
            'grant_type': 'refresh_token',
            'refresh_token': token["refresh_token"],
            'client_id': self.client_id
        }
        if refresh_type == "Refresh Token":
            reqData["access_type"] = "offline"

        # print(f"REFRESHING TOKEN: {data} - TRADER: {self.user['Name']} - REFRESH TYPE: {refresh_type} - ACCOUNT ID: {self.account_id}")

        response = requests.post(auth_url, reqData)

        if response.status_code != 200:
            if not self.no_go_token_sent:
                msg = f"ERROR WITH GETTING NEW TOKENS - {response.json()} - TRADER: {self.user['Name']} - REFRESH TYPE: {refresh_type} - ACCOUNT ID: {self.account_id}"
                self.logger.ERROR(msg)
                self.no_go_token_sent = True
            self.invalid_request_count += 1
            if self.invalid_request_count == 5:
                self.terminate = True
                msg = f"TDAMERITRADE INSTANCE TERMINATED - {response.json()} - TRADER: {self.user['Name']} - REFRESH TYPE: {refresh_type} - ACCOUNT ID: {self.account_id}"
                self.logger.ERROR(msg)
            return

        self.no_go_token_sent = False
        self.invalid_request_count = 0
        self.terminate = False

        return response.json()

























    def refresh_access_token(self):
        """
        Used to obtain a 30 minute API access_token
        :return: Json including access_token, expires_in, and time_created fields
        """
        auth_url = "https://api.tdameritrade.com/v1/oauth2/token"
        reqData = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
        }
        response = requests.post(auth_url, reqData)
        obj = {
            'time_created': time.strftime('%Y-%m-%d %H:%M %Z', time.localtime())
        }
        testJson = json.loads(response.content)
        testJson.update(obj)
        return testJson

    def get_accounts(self):
        """
        Fetches and prints a Json of all account details
        :return: [json]: account data
        """
        endpoint = "https://api.tdameritrade.com/v1/accounts"
        parameters = {
            'fields': 'positions,orders'
        }
        headers = {'Authorization': "Bearer {}".format(access_token)}
        response = requests.get(endpoint, headers=headers, params=parameters)
        print(json.dumps(response.json(), indent=4))

    def us_market_hours(self):
        endpoint = "https://api.tdameritrade.com/v1/marketdata/hours"
        headers = {'Authorization': "Bearer {}".format(access_token)}
        parameters = {
            'markets': 'EQUITY',
            'date': '2021-08-03'
        }
        response = requests.get(endpoint, headers=headers, params=parameters)
        print(json.dumps(response.json(), indent=4))