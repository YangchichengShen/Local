from collections import defaultdict
import praw
import os
from dotenv import load_dotenv
load_dotenv()

client_id= os.getenv("REDDIT_CLIENT_ID")
client_secret=os.getenv("REDDIT_CLIENT_SECRET")
redirect_uri='http://localhost:8501/Profile'
user_agent='Contextify/0.1 by Consistent_Gap_197'

def get_reddit_instance():
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        user_agent=user_agent
    )

def get_auth_url():
    reddit = get_reddit_instance()
    scopes = ['identity', 'history', 'mysubreddits']
    return reddit.auth.url(scopes=scopes, state='random_state_string', duration='temporary')

def auth_and_fetch_user(code):
    reddit = get_reddit_instance()
    print("Reddit client ID:", reddit._core._authorizer._authenticator.client_id)
    print("Redirect URI:", reddit._core._authorizer._authenticator.redirect_uri)
    print("User agent:", reddit.config.user_agent)
    reddit.auth.authorize(code)
    me = reddit.user.me()
    return me, reddit

weights = {
    "post": 3.0,
    "comment": 1.5,
    "subscribed": 1.0
}

def get_content(me, reddit):
    subreddit_scores = defaultdict(float)
    for post in me.submissions.new(limit=100):
        subreddit_scores[str(post.subreddit)] += weights["post"]
    for comment in me.comments.new(limit=100):
        subreddit_scores[str(comment.subreddit)] += weights["comment"]
    subscribed_subs = [sub.display_name for sub in reddit.user.subreddits(limit=50)]
    for sub in subscribed_subs:
        if sub not in subreddit_scores:
            subreddit_scores[sub] += weights["subscribed"]

    return subreddit_scores
    


