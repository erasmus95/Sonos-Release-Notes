#source reddit-poster/bin/activate

import json
import os
import praw
import requests

here = os.path.dirname(os.path.abspath(__file__))
credentials = os.path.join(here, 'client_secrets.json')
#credentials = 'client_secrets.json'

with open(credentials) as f:
    creds = json.load(f)

reddit = praw.Reddit(client_id=creds['client_id'],
                     client_secret=creds['client_secret'],
                     user_agent=creds['user_agent'],
                     redirect_uri=creds['redirect_uri'],
                     refresh_token=creds['refresh_token'])

subr = 'GregsSandbox' # Choose your subreddit
 
subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable
 
title = 'Just Made My first Post on Reddit Using Python.'
 
selftext = '''
I am learning how to use the Reddit API with Python using the PRAW wrapper.
By following the tutorial on https://www.jcchouinard.com/post-on-reddit-api-with-python-praw/
This post was uploaded from my Python Script
'''

class Reddit_Post:
    def __init__(self, title, body):
        self.title = title
        self.selftext = body


    def post_to_reddit(self):
        #print(self.title)
        #print(self.selftext)
        subreddit.submit(self.title,selftext=self.selftext)

#redditUpdate = Reddit_Post(title,selftext)
#redditUpdate.post_to_reddit()

#subreddit.submit(title,selftext=selftext)