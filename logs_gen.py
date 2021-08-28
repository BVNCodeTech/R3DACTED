from pymongo import MongoClient

client = MongoClient(
    f"")
db = client.CTCrypt
logs_collection = db['answer-entry-log']
users = db['users']

log_data = logs_collection.find()

bait_answers = ['chocofactory', 'rafaleisback', 'neigermonk', 'notionpictures', 'clintonkamani', 'sansisthebestfont',
                'battlegroundsmobileindia', 'doometernal2istheway', 'blenderfactory', 'rippedlabs']
cheaters = []
baited_ans = []

for user in log_data:
    user_data = users.find_one({'_id': user['_id']})
    level_count = 0
    filename = "".join(x for x in user['username'] if (x.isalnum() or x in "._- "))
    with open(f"logs/{filename}.txt", 'w') as user_file:
        try:
            user_file.writelines(f"""Name: {user_data['name']}
School: {user_data['organization']}
Discord: {user['username']}#{user['discriminator']}
Email: {user_data['email']}""")
        except UnicodeEncodeError:
            user_file.writelines(f"""Name: {user_data['name']}
School: {user_data['organization']}
Email: {user_data['email']}""")

        while True:
            try:
                level_log = user[f'level{level_count}']
                user_file.writelines(f"""\n--------
LEVEL {level_count}
--------""")
                level_count += 1
                for response in range(level_log['tries']):
                    try:
                        if level_log['responses'][f'response{response + 1}']['answer'] in bait_answers:
                            cheaters.append(user_data['_id'])
                            baited_ans.append(level_log['responses'][f'response{response + 1}']['answer'])
                        user_file.write(
                            f"\n[{level_log['responses'][f'response{response + 1}']['time']}] {level_log['responses'][f'response{response + 1}']['answer']}")
                    except UnicodeEncodeError:
                        user_file.write(
                            f"\n[{level_log['responses'][f'response{response + 1}']['time']}] Unidentified Character")
            except KeyError:
                break

with open('cheaters.txt', 'w') as paapi_list:
    print('subhogay')
    count = 0
    for paapi in cheaters:
        paapi_data = users.find_one({'_id': str(paapi)})
        paapi_list.write(f"\n{paapi_data['username']}#{paapi_data['discriminator']} [{baited_ans[count]}]")
        count += 1
