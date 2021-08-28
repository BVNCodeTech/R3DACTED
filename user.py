from pymongo import MongoClient
from flask import redirect, flash, session

client = MongoClient(
    f"")
db = client.CTCrypt
leaderboard = db["leaderboard"]
user_collection = db['users']
dq_collection = db['dq-participants']


def user_page(user_id):
    try:
        user = user_collection.find_one({'_id': user_id})
        lb_entry = leaderboard.find_one({'_id': user_id})
        data = {
            'username': user['username'],
            'name': user['name'],
            'organization': user['organization'],
            'time': user['time'],
            'level': lb_entry['level'],
            'last_solved': lb_entry['last_solved'],
        }
        return data
    except:
        flash("No matching user found!")
        return redirect('/play')


def admin_check(user_id):
    try:
        role = user_collection.find_one({'_id': session['user']})['role']
    except TypeError:
        role = 'participant'

    if role == "admin":
        return True
    else:
        return False


def dq_check(user_id):
    if dq_collection.find_one({'_id': user_id}):
        return True
    else:
        return False


def disqualify_user(user_id):
    if dq_collection.find_one({'_id': user_id}):
        return "User is already disqualified"
    else:
        current_points = leaderboard.find_one({'_id': user_id})['points']
        dq_collection.insert_one({'_id': user_id, 'points': current_points})
        leaderboard.update_one({'_id': user_id}, {'$set': {'points': 0}})
        return "Disqualified"


def requalify_user(user_id):
    if not dq_collection.find_one({'_id': user_id}):
        return "The user is already qualified"
    else:
        result = dq_collection.find_one({'_id': user_id})
        points = result['points']
        dq_collection.delete_one({'_id': user_id})
        leaderboard.update_one({'_id': user_id}, {'$set': {'points': points}})
        return "Requalified"


def change_role(user_id):
    if user_collection.find_one({'_id': user_id})['role'] == 'participant':
        user_collection.update_one({'_id': user_id}, {'$set': {'role': 'admin'}})
        return "Changed role to Admin"
    else:
        user_collection.update_one({'_id': user_id}, {'$set': {'role': 'participant'}})
        return "Changed role to Participant"
