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

# post a new tweet:
r = api.create_tweet(text="Hello world!")

# delete the tweet:
api.delete_tweet(tweet_id=r.id)

# search tweets on Comillas:
search = api.search_tweets(
    query='"Universidad Pontificia de Comillas"',
    max_results=10,
    tweet_fields=[
        "id",
        "author_id",
        "geo",
        "lang",
        "created_at"
    ]
)

for t in search.data:
    print(f"({t.created_at}) {t.id}: {t.text} => {t.geo}\n")


# get user data and timeline:
comillas_user = api.get_user(username="ucomillas")
comillas_activity = api.get_timelines(
    user_id=comillas_user.data.id,
    tweet_fields=["created_at"]
)

for t in comillas_activity.data:
    print(f"{t.created_at}: {t.text}")
