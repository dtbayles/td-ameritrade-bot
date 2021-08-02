import requests
import secrets
#from config import CLIENT_ID

import urllib.parse

refresh_token = {
  "access_token": secrets.access_token,
  "refresh_token": secrets.refresh_token,
  "scope": "PlaceTrades AccountAccess MoveMoney",
  "expires_in": 1800,
  "refresh_token_expires_in": 7776000,
  "token_type": "Bearer"
}

print(urllib.parse.quote(secrets.redirect_url))
print(urllib.parse.quote(secrets.client_id))

# https://localhost:8080/?code=


print(urllib.parse.unquote(secrets.code))

# https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http%3A//localhost%3A8080&client_id=3BQTAZGGRDEB1YIXPFBGRQPKL081SOSB%40AMER.OAUTHAP

reqData = {
    'grant_type': 'authorization_code',
    'access_type': 'offline',
    'client_id': secrets.client_id,
    'redirect_uri': secrets.redirect_url
}

# response = requests.post("https://api.tdameritrade.com/v1/oauth2/token", reqData)

# print(response)

def login(Consumer_Key):
    print("login function")