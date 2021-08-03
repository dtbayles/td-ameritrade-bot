import requests
import urllib.parse
import json
from secrets import access_token, redirect_uri, client_id, refresh_token

'''
How to generate a new refresh token if old one has completely expired (older than 90 days)
'''
def generate_refresh_token():
    auth_url = "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=" + urllib.parse.quote(redirect_uri) + "&client_id=" + urllib.parse.quote(client_id) + "%40AMER.OAUTHAP"
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

'''
To be used to obtain a 30 minute access_token
'''
def refresh_access_token():
    auth_url = "https://api.tdameritrade.com/v1/oauth2/token"
    reqData = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
    }
    response = requests.post(auth_url, reqData)
    print(response.content)

'''
Fetches and prints a Json of all account details
'''
def get_accounts():
    endpoint = "https://api.tdameritrade.com/v1/accounts"
    headers = {'Authorization': "Bearer {}".format(access_token)}
    response = requests.get(endpoint, headers=headers)
    print(json.dumps(response.json(), indent=4))

def US_market_hours():
    endpoint = "https://api.tdameritrade.com/v1/marketdata/hours"
    headers = {'Authorization': "Bearer {}".format(access_token)}
    parameters = {
        'markets': 'EQUITY',
        'date': '2021-08-03'
    }
    response = requests.get(endpoint, headers=headers, params=parameters)
    print(json.dumps(response.json(), indent=4))

US_market_hours()