import datetime
import plotly.express as px

import tweepy
import json

import pandas as pd


def get_credentials(file: dict):
    """Reads credential from json file
    :param file: JSON file with CONSUMER and ACCESS TOKE and SECRET values
    :return: dict
    """
    with open(file, "r") as file:
        result = json.load(file)
        return result


CREDS = get_credentials(file="auth/twitter_credentials.json")

AUTH = tweepy.OAuthHandler(
    CREDS["CONSUMER_KEY"],
    CREDS["CONSUMER_SECRET"]
)
AUTH.set_access_token(
    CREDS["ACCESS_TOKEN"],
    CREDS["ACCESS_SECRET"],
)

API_V1 = tweepy.API(
    auth=AUTH,
    wait_on_rate_limit=True,
)

API_V2 = tweepy.Client(
    bearer_token=CREDS["BEARER_TOKEN"],
    consumer_key=CREDS["CONSUMER_KEY"],
    consumer_secret=CREDS["CONSUMER_SECRET"],
    access_token=CREDS["ACCESS_TOKEN"],
    access_token_secret=CREDS["ACCESS_SECRET"],
    wait_on_rate_limit=True,
)


def example_v1_trends():
    public_tweets = API_V1.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    # available trends_
    trends = API_V1.available_trends()

    return trends


def example_v1_place_trends(woeid: int = 766273):
    # trens per location:
    trends = API_V1.get_place_trends(woeid)
    trends_df = pd.DataFrame(data=trends[0]["trends"])

    return trends, trends_df


def example_v1_get_user_info(username: str):
    # get user information:
    user = API_V1.get_user(screen_name=username)

    # counting total:
    followers_iterator = tweepy.Cursor(
        API_V1.get_followers,
        screen_name=username
    )

    follower_ids = []
    for t in followers_iterator.items():
        print(f"Adding user_id to the list...")
        follower_ids.append(t.id)

    return user, follower_ids


# region V2:

# Replace with your own search query
def example_v2_recent(
        query: str = 'from:suhemparack -is:retweet',
        tweet_fields: list = ['context_annotations', 'created_at'],
        max_results: int = 100,
):
    tweets = API_V2.search_recent_tweets(
        query=query,
        tweet_fields=tweet_fields,
        max_results=max_results,
    )

    return tweets


def example_v2_paginator(
        query: str = "djokovic -is:retweet lang:en",
        tweet_fields: list = [
            'context_annotations',
            'created_at',
            'author_id',
        ],
        max_results: int = 100,
        max_items: int = 1000,
        hist: bool = False,
):
    tweets = [
        tweet
        for tweet in tweepy.Paginator(
            API_V2.search_recent_tweets,
            query=query,
            tweet_fields=tweet_fields,
            max_results=max_results).flatten(limit=max_items)
    ]

    return tweets


def example_histogram(tweets: list):
    data = [{"date": d.created_at, "text": d.text} for d in tweets]

    words = [
        d["text"].split()
        for d in data
    ]
    words = sum(words, [])

    df = pd.DataFrame({"words": words})
    fig = px.histogram(df, x="words").update_xaxes(categoryorder="total descending")
    fig.show()


def example_v2_timeline(
        id: str = "398306220",
        tweet_fields: list = [
            "id",
            "created_at",
            "public_metrics",
            # "context_annotations",
        ],
        max_results: int = 50,
        max_items: int = 150,
        start_time=(datetime.datetime.now(datetime.timezone.utc)
                    - datetime.timedelta(days=7)),
):
    tweets = [
        tweet
        for tweet in tweepy.Paginator(
            API_V2.get_users_tweets,
            id=id,
            start_time=start_time.strftime("%Y-%m-%dT00:00:00+00:00"),
            tweet_fields=tweet_fields,
            max_results=max_results).flatten(limit=max_items)
    ]

    return tweets


def example_v2_followers(
        user_id: str = "398306220",
        max_results: int = 50,
        max_items: int = 150,
):
    followers = [
        tweet
        for tweet in tweepy.Paginator(
            API_V2.get_users_followers,
            id=user_id,
            max_results=max_results).flatten(limit=max_items)
    ]

    return followers