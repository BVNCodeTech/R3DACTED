from pymongo import MongoClient
from flask import session, redirect

client = MongoClient(
    f"")
db = client.CTCrypt
user_collection = db['users']
leaderboard = db['leaderboard']


def user_data_upload(name, org):
    search_query = {'_id': session['user']}
    update_query = {
        '$set': {
            'name': name,
            'organization': org
        }
    }
    user_collection.update_one(search_query, update_query)
    update_query = {
        '$set': {
            'level': 0
        }
    }
    leaderboard.update_one(search_query, update_query)
    return redirect('/play')
