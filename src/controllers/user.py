from src.app import app
from src.config import DBURL
from pymongo import MongoClient
from bson.json_util import dumps
from flask import request
import datetime
from src.helpers.errorHandler import errorHandler, APIError
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords


client = MongoClient(DBURL)
db = client.get_database()

#TEST FUNCITON
@app.route('/')
def hello():
    return 'Welcome to the chat recommender!'

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
    return {'result':dumps(check)}


@app.route('/user/<name>')
@errorHandler
def get_user(name):
    user = db.users.find_one({'name':name},{'chats':0})
    if user == None:
        raise APIError ("The user does not exist, you can create it by using the endpoint /user/create/<name>")
    
    chat = db.users.find_one({'name':name},{'chats':1, '_id':0})['chats']

    chats = []
    for e in chat:
        chats.append(db.chats.find_one({'_id': e}, {'name':1, '_id':0})['name'])
        
    return {'user' : dumps(user),
            'user_chats' : chats}
        

@app.route('/user/<name>/sentiment/')
def sentiment_user(name):
    sia = SentimentIntensityAnalyzer()
    stpwrd = set(stopwords.words('english'))
    user_id = db.users.find_one({'name':name}, {'_id':1})['_id']
    cur = db.messages.find({'user':user_id}, {'text':1, '_id':0})
    text = ' '.join([e['text'] for e in cur]).split(' ')
    trimmed = ''
    for w in text:
        if w not in stpwrd:
            trimmed += w + ' '
    return sia.polarity_scores(trimmed)
  


