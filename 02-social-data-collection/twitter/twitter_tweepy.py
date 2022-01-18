import time

import tweepy
import json

import pandas as pd

with open("auth/twitter_credentials_teaching.json", "r") as file:
    credentials = json.load(file)

auth = tweepy.OAuthHandler(
    credentials["CONSUMER_KEY"],
    credentials["CONSUMER_SECRET"]
)
auth.set_access_token(
    credentials["ACCESS_TOKEN"],
    credentials["ACCESS_SECRET"],
)

api = tweepy.API(
    auth=auth,
    wait_on_rate_limit=True,
)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# available trends_
trends = api.available_trends()


# trens per location:
madrid_woeid = 766273
trends_madrid = api.get_place_trends(madrid_woeid)
trends_madrid_df = pd.DataFrame(data=trends_madrid[0]["trends"])

# get user information:
comillas_screen_name = "ucomillas"
comillas_user = api.get_user(screen_name=comillas_screen_name)

# counting total:
followers_iterator = tweepy.Cursor(
    api.get_followers,
    screen_name=comillas_screen_name
)

follower_ids = []
for t in followers_iterator.items():
    print(f"Adding user_id to the list...")
    follower_ids.append(t.id)

