from src.app import app
from src.config import DBURL
from pymongo import MongoClient


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
def create_usr():
    pass



@app.route('/')
def hola():
    return {'Ole': 'esta es tu api'}

