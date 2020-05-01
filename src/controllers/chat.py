from src.app import app
from src.config import DBURL
from pymongo import MongoClient
from flask import request
from bson.json_util import dumps
from src.helpers.errorHandler import APIError, errorHandler


client = MongoClient(DBURL)
db = client.get_database()



@app.route('/chat/list/')
def list_chat():
    lst = db.chats.find({})
    return dumps([chat for chat in lst])


@app.route('/chat/create/<name>')
@errorHandler
def create_chat(name):
    '''
    Insert a new chat and check 
    that it has been correctly inserted by returning 
    a find_one. The function checks for unique names and can insert one participant as 
    a parameter users
    '''
    cur = db.chats.find({}, {'name':1})
    if name in [n['name'] for n in cur]:
        raise APIError ('That name is already in use, please use another name')
    db.chats.insert_one({'name':name, 'participants':[]})
    if request.args:
        for u in request.args:
            user = request.args[u]
            id = db.users.find_one({'name':user},{'_id':1})['_id']
            db.chats.update({'name': name },{'$addToSet': {'participants': id } })
    check = db.chats.find_one({'name': name})
    return {
        'message': 'We succeded in creating the chat!',
        'result': dumps(check)
        }


@app.route('/chat/add_user/')
@errorHandler
def add_user():
    chat = request.args['chat']
    user = request.args['user']
    cur = db.chats.find({}, {'name':1})
    if chat not in [n['name'] for n in cur]:
        raise APIError ('That chat does not exist, you can create it with the endpoint /chat/create/<chat_name>')
    cur = db.users.find({}, {'name':1})
    if user not in [n['name'] for n in cur]:
        raise APIError ('That user does not exist, you can create it with the endpoint /user/create/<user_name>')
    
    id_chat = db.chats.find_one({'name':chat},{'_id':1})['_id']
    id_user = db.users.find_one({'name':user},{'_id':1})['_id']

    cur = db.chats.find({'_id':id_chat}, {'participants':1})
    if id_user  in [e['participants'] for e in cur ][0]:
        raise APIError ('That user is already in the chat')

    db.chats.update({'_id': id_chat },{'$addToSet': {'participants': id_user } })
    return {'Chat': dumps(db.chats.find_one({'name':chat})),
            'Message': 'We succeded in adding the user'
    }
