#source reddit-poster/bin/activate
import json
import praw
'''credentials_filename = 'client_secrets.json'
here = os.path.dirname(os.path.abspath(__file__))

credentials = os.path.join(here, credentials_filename)

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
#    I am learning how to use the Reddit API with Python using the PRAW wrapper.
#    By following the tutorial on https://www.jcchouinard.com/post-on-reddit-api-with-python-praw/
#    This post was uploaded from my Python Script
'''
'''

class Reddit_Post:
    def __init__(self, title, body, subr, credentials_path):
        self.title = title
        self.selftext = body
        self.subr = subr
        self.credentials = credentials_path
        
    def post_to_reddit(self):
        with open(self.credentials) as f:
            creds = json.load(f)

        reddit = praw.Reddit(
                            client_id=creds['client_id'],
                            client_secret=creds['client_secret'],
                            user_agent=creds['user_agent'],
                            redirect_uri=creds['redirect_uri'],
                            refresh_token=creds['refresh_token']
                            )
        
        subreddit = reddit.subreddit(self.subr) # Initialize the subreddit to a variable

        subreddit.submit(self.title,selftext=self.selftext)