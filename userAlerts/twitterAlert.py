import requests
import tweepy

class TwitterCommunicator:
    def __init__(self):
        # Handle authorization for the Twitter API
        auth = tweepy.OAuthHandler("OJCwZkO2oHJ9KkxBuRz9PQyOa", 
                                    "Ws5aJZANI6tVw53nEvCl7B5cyceB6N8wqhdD3hPluy7IXkPd0t")
        auth.set_access_token("3324006958-V0DcjTUL138TMI2MGaA9Cb5iAQQugqYiQsBiEaT",
                                "2GNE4Bzfc6PeEAZliVoH8L48vIys8m2VOoRaR6Dtmg0JA")
        # Add an instance of the api to class variables as well as the current authenticated 
        # user's id
        self.api = tweepy.API(auth)
        self.user = self.api.me().id

    '''
    Sends a dm to the user.
    @param {message}  REQUIRED        - The desired message to send
    @param {user}  NOT REQUIRED    - The id of the user to be dm'd. default is authenticated user 
    '''
    def directMessage(self, message, user=None):
        if (user is not None):
            self.api.send_direct_message(user, message)
        
        else:
            self.api.send_direct_message(self.user, message)