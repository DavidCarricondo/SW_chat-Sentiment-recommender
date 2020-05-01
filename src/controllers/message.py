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

    id_chat = db.chats.find_one({'name':chat},{'_id':1})['_id']
    id_user = db.users.find_one({'name':user},{'_id':1})['_id']

    db.messages.insert_one({'chat': id_chat,'user': id_user,'time': str(datetime.datetime.now()),'text': text})

    return {'message':'We succeeded in adding the text',
            'entry': dumps(db.messages.find_one({'text':text}))
            }


@app.route('/message/list/<chat>')
@errorHandler
def list_messages(chat):

    id_chat = db.chats.find_one({'name':chat},{'_id':1})['_id']
    messages = db.messages.find({'chat':id_chat})
    
    return dumps(messages)


