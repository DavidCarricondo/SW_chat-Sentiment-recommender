from src.app import app
from src.config import DBURL
from pymongo import MongoClient
from flask import request
from bson.json_util import dumps
from src.helpers.errorHandler import APIError, errorHandler
import datetime


client = MongoClient(DBURL)
db = client.get_database()



@app.route('/message/<user>/add/')
@errorHandler
def add_message(user):
    chat = request.args['chat']
    text = request.args['text']

    #Check that the user exist
    cur = db.users.find({}, {'name':1})
    if user not in [n['name'] for n in cur]:
        raise APIError ('That user does not exist, you can create it with the endpoint /user/create/<user_name>')

    id_chat = db.chats.find_one({'name':chat},{'_id':1})['_id']
    id_user = db.users.find_one({'name':user},{'_id':1})['_id']

    #Check that the user exist in the chat and otherwise, include it:
    participants = db.chats.find_one({'$and':[{'_id':id_chat},{'participants':id_user}]})
    if participants == None:
            db.chats.update({'_id': id_chat },{'$addToSet': {'participants': id_user } })
            message = 'We succeded in adding the message and added the user to the chat'
    else: message = 'We succeded in adding the message'
    
    #Insert the message
    db.messages.insert_one({'chat': id_chat,'user': id_user,'time': str(datetime.datetime.now()),'text': text})
    db.users.update({'_id': id_user},{'$addToSet': {'chats': id_chat } })

    return {'status': message,
            'entry': dumps(db.messages.find_one({'text':text}))}
 


@app.route('/message/<chat>/list/')
@errorHandler
def list_messages(chat):

    id_chat = db.chats.find_one({'name':chat},{'_id':1})['_id']
    messages = db.messages.find({'chat':id_chat})
    result = {}
    for i,e in enumerate(messages):
        result[i] = {'name': db.users.find_one({'_id':e['user']},{'_id':0, 'name':1})['name'],
                    'time': e['time'],
                    'text':e['text']}
    return result

