from src.app import app
from src.helpers.errorHandler import errorHandler
from sklearn.feature_extraction.text import CountVectorizer
from src.config import DBURL
from pymongo import MongoClient
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
from nltk.corpus import stopwords


client = MongoClient(DBURL)
db = client.get_database()

@app.route('/user/<user>/recommend')
@errorHandler
def recommender(user):
    #Create a dictionary with all the messages of each user
    messages = {}
    users = db.users.find({}, {'_id':1, 'name':1})
    for e in users:
        texts = db.messages.find({'user':e['_id']}, {'text':1,'_id':0})
        messages[e['name']] = ' '.join([t['text'] for t in texts])

    #Remove stopwords from the messages:
    trimmed = {}
    stpwrd = set(stopwords.words('english'))
    string = ''
    for k,v in messages.items():
        trimmed[k]=' '.join([w for w in v.split(' ') if w not in stpwrd]) 
    #Create a sparse_matrix with the counts of each word for each of the users 
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(trimmed.values())
    matrix = sparse_matrix.todense()

    #Calculate the cosine distances between users:
    similarity_matrix = distance(matrix, matrix)
    sim_df = pd.DataFrame(similarity_matrix, columns=messages.keys(), index=messages.keys())

    similars = sim_df[user].sort_values(ascending=False)[1:].head(3)
    return {'Similar users': list(similars.index)}