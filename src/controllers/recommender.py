from src.app import app
from src.helpers.errorHandler import errorHandler, APIError
from sklearn.feature_extraction.text import CountVectorizer
from src.config import DBURL
from pymongo import MongoClient
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
from scipy.spatial.distance import pdist, squareform
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from flask import request



client = MongoClient(DBURL)
db = client.get_database()

@app.route('/user/<user>/recommend')
@errorHandler
def recommender(user):

    if not request.args:
        raise APIError ('This endpoint requires a paramether type= "similar" or type="sentiment"')

    type_recom = request.args['type']

    if type_recom not in ['similar', 'sentiment']:
        raise APIError ('The type parameter must be either "similar" or "sentiment"')

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

    if type_recom == 'similar':
        #Create a sparse_matrix with the counts of each word for each of the users 
        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(trimmed.values())
        matrix = sparse_matrix.todense()

        #Calculate the cosine distances between users:
        similarity_matrix = distance(matrix, matrix)
        sim_df = pd.DataFrame(similarity_matrix, columns=messages.keys(), index=messages.keys())

        similars = sim_df[user].sort_values(ascending=False)[1:].head(3)
        return {'Similar users': list(similars.index)}

    elif type_recom == 'sentiment':
        sia = SentimentIntensityAnalyzer()
        sentim = {}
        for k, v in trimmed.items():
            sentim[k] = sia.polarity_scores(v)
        simi =pd.DataFrame(sentim).T
        distances = pd.DataFrame(1/(1+ squareform(pdist(simi, 'euclidean'))), index=simi.index, columns=simi.index)
        similars = distances[user].sort_values(ascending=False)[1:].head(3)
        return {'Similar users': list(similars.index)}
