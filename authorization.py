import pymongo
from pymongo import MongoClient
import requests
from flask import session, flash, redirect
from datetime import datetime
import pytz

UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')

client = MongoClient(
    "")
db = client.CTCrypt
user_collection = db['users']
leaderboard = db['leaderboard']
answer_log = db['answer-entry-log']


def authorize(token):
    try:
        headers = {'Authorization': f"Bearer {token}"}
        user_data = requests.get('https://discordapp.com/api/users/@me', headers=headers)
        user_connections = requests.get('https://discordapp.com/api/users/@me/connections', headers=headers)
        success = True
    except:
        raise Exception("Failed to fetch data from the Discord Endpoints")

    if success:
        user_data = user_data.json()
        user_id = user_data['id']
        del user_data['id']
        del user_data['public_flags']
        del user_data['flags']
        del user_data['locale']
        user_data['_id'] = user_id

        datetime_ist = datetime.now(IST)
        time = datetime_ist.strftime('%d/%m/%Y %H:%M:%S %Z %z')

        leaderboard_entry = user_data.copy()
        leaderboard_entry['level'] = '-'
        leaderboard_entry['last_solved'] = time
        leaderboard_entry['points'] = 0
        del leaderboard_entry['mfa_enabled']
        del leaderboard_entry['avatar']
        del leaderboard_entry['verified']

        log_entry = user_data.copy()
        del log_entry['mfa_enabled']
        del log_entry['avatar']
        del log_entry['verified']
        log_entry['level0'] = {
            'tries': 0,
            'time_reached': time,
            'responses': {}
        }

        user_data['time'] = time
        user_data['name'] = '-'
        user_data['organization'] = '-'
        user_data['role'] = 'participant'

        user_connections = user_connections.json()

        if len(user_connections) != 0:
            for index in range(len(user_connections)):
                connection = user_connections[index]
                social = connection['type']
                del connection['type']
                user_data[social] = connection

        try:
            answer_log.insert_one(log_entry)
            leaderboard.insert_one(leaderboard_entry)
            user_collection.insert_one(user_data)
            session['login'] = True
            session['user'] = user_id
            flash("Registration Successful", 'correct-ans')
            return redirect('/')
        except pymongo.errors.DuplicateKeyError:
            result = user_collection.find_one({'_id': user_id})
            if user_data['email'] != result['email'] or user_data['username'] != result['username'] or user_data[
                'discriminator'] != result['discriminator']:
                search_query = {'_id': user_id}
                update_query = {'$set': {
                    'email': user_data['email'],
                    'username': user_data['username'],
                    'discriminator': user_data['discriminator'],
                    'avatar': user_data['avatar']
                }}
                user_collection.update_one(search_query, update_query)

            session['login'] = True
            session['user'] = user_id
            flash("Logged in successfully", 'correct-ans')
            return redirect('/')
        except:
            session['login'] = False
            session['user'] = None
            flash("Failed to register user", 'incorrect-ans')
            return redirect('/')
