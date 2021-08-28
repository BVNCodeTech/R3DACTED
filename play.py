from datetime import datetime
import pytz
from flask import redirect, session, flash
from pymongo import MongoClient

UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')

client = MongoClient(
    f"")
db = client.CTCrypt
user_collection = db['users']
leaderboard = db['leaderboard']
questions = db['questions']
answer_log = db['answer-entry-log']
dq_collection = db['dq-participants']
checking_collection = db['checker']


def login_check(check):
    if check:
        session['question_display'] = True
    else:
        return redirect('/auth')


def get_level():
    user = leaderboard.find_one({'_id': session['user']})
    level = user['level']
    return f"Level {level}"


def get_level_content():
    user = leaderboard.find_one({'_id': session['user']})
    level = user['level']
    session['level'] = level
    if level == '-':
        return None
    else:
        try:
            question_doc = questions.find_one({'_id': level})
            question = question_doc['question']
            return f"{question}"
        except:
            end = "True"
            return end


def get_level_image():
    user = leaderboard.find_one({'_id': session['user']})
    level = user['level']
    session['level'] = level
    if level == '-':
        return None
    else:
        try:
            question_doc = questions.find_one({'_id': level})
            image = question_doc['image']
            return image
        except:
            end = "True"
            return end


def validate_answer(response, ip):
    user_lb = leaderboard.find_one({'_id': session['user']})
    current_level = user_lb['level']
    current_points = user_lb['points']
    question_doc = questions.find_one({'_id': current_level})
    next_level = int(question_doc['next_level'])
    datetime_ist = datetime.now(IST)
    time = datetime_ist.strftime('%d/%m/%Y %H:%M:%S %Z %z')
    search_query = {'_id': session['user']}
    points = question_doc['points']

    # live logs
    print(f"[{user_lb['username']}] Level-{current_level} ---> {response} @{time}")

    user_input = response.lower().replace(' ', '')
    user_input = ''.join(char for char in user_input if char.isalnum())
    if user_input == question_doc['answer']:

        update_query = {'$set': {
            'level': next_level,
            'last_solved': time,
            'points': current_points + points,
        }
        }
        leaderboard.update_one(search_query, update_query)

        user_log = answer_log.find_one({'_id': session['user']})
        tries = user_log[f'level{current_level}']['tries']

        current_lvl_data = user_log[f'level{current_level}']
        current_lvl_data['responses'][f'response{tries + 1}'] = {
            'answer': user_input,
            'time': time,
            'ip': ip,
        }
        current_lvl_data['tries'] = tries + 1

        update_query = {'$set': {
            f'level{current_level}': current_lvl_data
        }
        }
        answer_log.update_one(search_query, update_query)

        update_query = {'$set': {
            f'level{current_level + 1}': {
                'tries': 0,
                'time_reached': time,
                'responses': {}
            }}}
        answer_log.update_one(search_query, update_query)
        flash("Correct answer!", 'correct-ans')
        return redirect('/play')

    else:
        user_log = answer_log.find_one({'_id': session['user']})
        tries = user_log[f'level{current_level}']['tries']
        current_lvl_data = user_log[f'level{current_level}']
        current_lvl_data['responses'][f'response{tries + 1}'] = {
            'answer': user_input,
            'time': time,
            'ip': ip,
        }
        current_lvl_data['tries'] = tries + 1

        update_query = {'$set': {
            f'level{current_level}': current_lvl_data
        }
        }
        answer_log.update_one(search_query, update_query)
        flash("Incorrect answer!", 'incorrect-ans')
        return redirect('/play')


def checkifrunning():
    status_check = checking_collection.find_one({'_id': 'checker'})
    status = status_check['checker']
    return status
