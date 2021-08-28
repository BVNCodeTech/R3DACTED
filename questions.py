from flask import redirect, session, flash
from pymongo import MongoClient

client = MongoClient(
    f"")
db = client.CTCrypt
user_collection = db['users']
question_collection = db['questions']


def fetch_questions(id=None):
    if id != None:
        question_data = question_collection.find_one({'_id': int(id)})
        return question_data
    else:
        questions = []
        questions_data = question_collection.find()
        if questions_data:
            for question in questions_data:
                try:
                    questions.append({
                        'content': question['question'],
                        'answer': question['answer'],
                        'image': question['image'],
                        'points': int(question['points']),
                        'next_level': int(question['next_level'])
                    })
                except KeyError:
                    questions.append({
                        'content': question['question'],
                        'answer': question['answer'],
                        'image': '',
                        'points': int(question['points']),
                        'next_level': int(question['next_level'])
                    })
        return questions


def add_question(id, content, image, answer, points, next_level):
    question_collection.insert_one(
        {'_id': int(id), 'question': content, 'image': image, 'answer': answer, 'points': int(points),
         'next_level': int(next_level)})
    return "Added question"


def edit_question(id, content=None, image=None, answer=None, points=None, next_level=None):
    question = question_collection.find_one({'_id': int(id)})
    content_old = question['question']
    try:
        image_old = question['image']
    except KeyError:
        image_old = ''
    answer_old = question['answer']
    points_old = int(question['points'])
    next_level_old = int(question['next_level'])
    new_data = [int(id), content, image, answer, int(points), int(next_level)]
    update = {'$set': {
        'question': content if new_data[1] else content_old,
        'image': image if new_data[2] else image_old,
        'answer': answer if new_data[3] else answer_old,
        'points': points if new_data[4] else points_old,
        'next_level': next_level if new_data[5] else next_level_old
    }}
    question_collection.update_one({'_id': int(id)}, update)
    return f"Modified question {id}"
