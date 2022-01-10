import json
from pytwitter import Api

# Load credentials from json file
with open("auth/twitter_credentials.json", "r") as file:
    credentials = json.load(file)

# Instantiate the API object
api = Api(
    consumer_key=credentials["CONSUMER_KEY"],
    consumer_secret=credentials["CONSUMER_SECRET"],
    access_token=credentials["ACCESS_TOKEN"],
    access_secret=credentials["ACCESS_SECRET"]
)

# search:
query_str = "learn python"

tweets = api.search_tweets(
    query=query_str,
    tweet_fields=[
        "id",
        "author_id",
        "geo",
        "lang",
    ]
)

single_tweet = tweets.data[0]
print(single_tweet.to_json())

r = api.create_tweet(text="Hello world!")

api.delete_tweet(tweet_id=r.id)