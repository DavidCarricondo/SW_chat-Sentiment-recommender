from src.app import app
from src.config import DBURL
from pymongo import MongoClient
from bson.json_util import dumps


client = MongoClient(DBURL)
db = client.get_database()



@app.route('/chat/list/')
def list_chat():
    lst = db.chat.find({})
    return dumps([chat for chat in lst])

@app.route('/chat/create/<name>')
def create_chat(name):
    '''
    Insert a new chat and check 
    that it has been correctly inserted by returning 
    a find_one
    '''
    db.chat.insert_one({'name':name, 'participants':[]})
    check = db.chat.find_one({'name': name})
    return dumps(check)