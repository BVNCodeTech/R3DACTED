from pymongo import MongoClient, collection

client = MongoClient(
    f"")
db = client.CTCrypt
collection = db['checker']


def runhunt():
    search = {'_id': 'checker'}
    update = {'$set': {
        'checker': 'running'
    }
    }
    collection.update_one(search, update)


def endhunt():
    search = {'_id': 'checker'}
    update = {'$set': {
        'checker': 'ended'
    }
    }
    collection.update_one(search, update)


def pausehunt():
    search = {'_id': 'checker'}
    update = {'$set': {
        'checker': 'paused'
    }
    }
    collection.update_one(search, update)
