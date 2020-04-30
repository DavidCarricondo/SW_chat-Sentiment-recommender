from src.app import app
from src.config import DBURL
from pymongo import MongoClient
from bson.json_util import dumps


client = MongoClient(DBURL)
db = client.get_database()


@app.route('/user/collections/')
def collections():
    '''
    THis function only checks the collections in the database
    to make sure that the connection is correct
    '''
    col = db.list_collections()
    return {'collections':[c['name'] for c in col]}
        

@app.route('/user/create/<name>')
def create_usr(name):
    '''
    Insert a new user and check 
    that it has been correctly inserted by returning 
    a find_one. Need to check for repeated users.
    '''
    db.users.insert_one({'name':name, 'chats':[]})
    check = db.users.find_one({'name': name})
    return dumps(check)



@app.route('/')
def hola():
    return {'Ole': 'esta es tu api'}

