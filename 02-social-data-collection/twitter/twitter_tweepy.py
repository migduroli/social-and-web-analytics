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

api = tweepy.API(auth)

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
comillas_user = api.get_user(screen_name="ucomillas")