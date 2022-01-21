import time

import tweepy
import json

import pandas as pd

with open("auth/twitter_credentials_ext.json", "r") as file:
    credentials = json.load(file)

auth = tweepy.OAuthHandler(
    credentials["CONSUMER_KEY"],
    credentials["CONSUMER_SECRET"]
)
auth.set_access_token(
    credentials["ACCESS_TOKEN"],
    credentials["ACCESS_SECRET"],
)

# V1:
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


# V2:
client = tweepy.Client(
    bearer_token=credentials["BEARER_TOKEN"],
    consumer_key=credentials["CONSUMER_KEY"],
    consumer_secret=credentials["CONSUMER_SECRET"],
    access_token=credentials["ACCESS_TOKEN"],
    access_token_secret=credentials["ACCESS_SECRET"]
)

# Replace with your own search query
query = 'from:suhemparack -is:retweet'

# Replace with time period of your choice
start_time = '2020-01-01T00:00:00Z'

# Replace with time period of your choice
end_time = '2020-08-01T00:00:00Z'

tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                  start_time=start_time,
                                  end_time=end_time, max_results=100)


query = 'covid -is:retweet'

tweets = []
for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=[
                                  'context_annotations',
                                  'created_at'
                              ], max_results=100).flatten(limit=1000):
    tweets.append(tweet)
