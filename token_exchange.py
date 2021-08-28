from config import *
from flask import request, redirect, session
import requests


def get_token():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identity email connections'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(f'https://discord.com/api/v6/oauth2/token', data=data, headers=headers)
    r.raise_for_status()
    session['token'] = r.json()['access_token']
    return redirect('/fetch-userdata')
