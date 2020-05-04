
<img src="./INPUT/hqdefault.jpg" alt="Pussies with swords" title="May the 4th be with you" width="2000" height="300" />

# API-chat-recommender: STAR WARS EDITION

This is an API for data extraction, user recommendation, and sentiment analysis of a chat. The API is deployed as a docker container in a Heroku server using a MongoDB Atlas database in the cloud.

As a homage of the release date (May 4th), the database has been populated with dialogues from Star Wars Episode IV. The the Jupyter notebook `Populating_database.ipynb` describe the steps to populate the database.

The Jupyter notebook `API_test.ipynb` is a walkthrough all the endpoints of the API describe below.


## Endpoints

The return of the endpoints are in JSON format.

### **General url**

The general url is `http://api-project-ih.herokuapp.com`. 

A request to this url will return a welcome message to the API.

### **Chat endpoints**

*   **List the chats in the database**

        '/chat/list/'

*   **Create a new chat**


        '/chat/create/<name>'
    
    Paramethers (Optional):
    user:\<user-name> As many instances as desired. Adds one or more users to the new chat. 
     
*   **Add existing user to existing chat:**

        '/chat/add_user/'
    Paramethers (mandatory):

    chat=\<chat-name>

    user=\<user-name>

*   **Run a sentiment analysis of a chat:**

        '/chat/<chat-name>/sentiment/'
    The response is the typical response of a sentiment analysis:

    +   pos: positive index

    +   neg: negative index:

    +   neu: neutral index

    +   compound: general direction (x>0 : positive tendency; x<0 : negative tendency)

### **User endpoints**

*   **Add a new user to the database**

        '/user/create/<name>'

*   **Run a sentiment analysis of the messages from an existing user**

        '/user/<name>/sentiment/'

*   **Recommend similar users to an existing user**

        '/user/<user>/recommend'

    Paramether (mandatory):
    
    type=\<type-of-recommender> (sentiment or similar)
            
    *   *type=similar* will run a recommender based on the similarity of the content of the messages from each user.
    *   *type=sentiment* will run a recommender based on a sentiment analysis of the messages from each user.

### **Message endpoints**

*   **List the messages from an existing chat**

        '/message/<chat>/list/'

*   **Add a new message from a user to an existing chat**

        '/message/<user>/add/'

    Paramethers (mandatory):

    chat=\<chat-name>
    
    text=\<body-of-the-message>

    The user must be an existing user, however, if the user was not part of the participants of that chat, it will be included. 

### **TO-DO**

*   Recommend only users that have not interacted with the target user.

*   Refactor functions and add error handlings in some of them.

*   Redefine returns of POST functions as HTML to be more human readable

*   It's possible that with a greater load of messages and users the recommender's calculation takes some time,
        maybe is a good idea to optimize it taking the calculation of the distance matrix outside of the function. 

        
                           MAY THE 4TH BE WITH YOU
