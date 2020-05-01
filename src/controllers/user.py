from src.app import app
from src.config import DBURL
from pymongo import MongoClient
from bson.json_util import dumps
from flask import request
import datetime
from src.helpers.errorHandler import errorHandler, APIError


client = MongoClient(DBURL)
db = client.get_database()

@app.route('/user/create/<name>')
@errorHandler
def create_usr(name):
    us = db.users.find({},{'name':1})
    users = [u['name'] for u in us]
    if name in users:
        raise APIError ("The user already exist, please use a different name")
    '''
    Insert a new user and check 
    that it has been correctly inserted by returning 
    a find_one. Need to check for repeated users.
    '''
    db.users.insert_one({'name':name, 'created':str(datetime.datetime.now()), 'chats':[]})
    check = db.users.find_one({'name': name})
    return dumps(check)


@app.route('/user/<name>')
@errorHandler
def get_user(name):
    user = db.users.find_one({'name':name})
    if user:
            return dumps(user)
    else:
        raise APIError ("The user does not exist, you can create it by using the endpoint /user/create/<name>")
  


        