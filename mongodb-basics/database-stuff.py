from flask import Flask
from pymongo import MongoClient
from bson import json_util
from json import loads

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['mongodb-basics']

# results = db.users.insert_one({ 'name': 'Sue', 'username': 'sueiscool'})
# print(results.inserted_id)

@app.get('/users')
def get_all_users():
    result = db.users.find()
    return loads(json_util.dumps(result))
