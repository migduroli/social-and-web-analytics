import json
import requests

from enum import Enum
from typing import Union, Optional
from authlib.integrations.requests_client import (
    OAuth1Auth,
    OAuth2Auth,
)
from urllib.parse import urlencode

BASE_API_URL_V2 = "https://api.twitter.com/2"
TWEETS_URL_V2 = f"{BASE_API_URL_V2}/tweets"

SESSION = requests.Session()


def load_credentials(file_path: str) -> dict:
    """Load credentials from json file
    :param file_path: path to the JSON file where the credentials are securely stored
    :return: Dict with the credential details with the following structure:
        {
          "CONSUMER_KEY": "YOUR_APP_KEY",
          "CONSUMER_SECRET": "YOUR_APP_SECRET_KEY",
          "ACCESS_TOKEN": "YOUR_ACCESS_TOKEN",
          "ACCESS_SECRET": "YOUR_ACCESS_SECRET_TOKEN"
        }
    """
    with open(file_path, "r") as file:
        creds = json.load(file)
    return creds


def get_app_auth(access_token: str) -> OAuth2Auth:
    """It instantiates an OAuth2Auth object given the credentials passed in `args`

    :param access_token: The access token required

    :return: OAuth2Auth object
    """
    r = OAuth2Auth(
        token={
            "access_token": access_token,
            "token_type": "Bearer"},
    )
    return r


def get_user_auth(
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_secret: str,
) -> OAuth1Auth:
    """It instantiates an OAuth1Auth object given the credentials passed in `args`

    :param consumer_key: The API_KEY generated for our twitter app
    :param consumer_secret: The API_SECRET generated for our twitter app
    :param access_token: The ACCESS_TOKEN generated for our twitter app
    :param access_secret: The ACCESS_SECRET generated for our twitter app

    :return: OAuth1Auth object
    """
    r = OAuth1Auth(
        client_id=consumer_key,
        client_secret=consumer_secret,
        token=access_token,
        token_secret=access_secret,
    )
    return r


def get_tweets(ids: list, auth: Union[OAuth1Auth, OAuth2Auth]):
    query = {"ids": ",".join(ids)}
    search = SESSION.request(
        url=f"{TWEETS_URL_V2}?{urlencode(query)}",
        method="GET",
        auth=auth,
    ).json()
    return search


def search_tweets(query: dict, auth: Union[OAuth1Auth, OAuth2Auth]):
    search = SESSION.request(
        url=f"{TWEETS_URL_V2}/search/recent?{urlencode(query)}",
        method="GET",
        auth=auth,
    ).json()
    return search


class TweetAction(Enum):
    POST = 1
    DELETE = 2


def tweet(
        action: TweetAction,
        auth: OAuth1Auth,
        id: Optional[str] = None,
        data: Optional[dict] = None
):
    url = f"{TWEETS_URL_V2}/{id}" \
        if id and (action == TweetAction.DELETE) \
        else TWEETS_URL_V2

    r = SESSION.request(
        url=url,
        method=action.name,
        json=data,
        auth=auth,
    ).json()
    return r


credentials = load_credentials(
    file_path="auth/twitter_credentials.json",
)

app_auth = get_app_auth(
    access_token=credentials["BEARER_TOKEN"],
)

id_list = ["1261326399320715264"]
tweets = get_tweets(ids=id_list, auth=app_auth)

# Now you can explore the results of this search:
# tweets["data"]

# Example of a more complex query:
query_text = {"query": '"learn python" lang:en',
              "tweet.fields": "id,author_id,geo,lang,public_metrics",
              "max_results": 50}

tweets = search_tweets(query=query_text, auth=app_auth)

# As in the previous case, we can now explore the results:
# tweets["data"]

user_auth = get_user_auth(
    consumer_key=credentials["CONSUMER_KEY"],
    consumer_secret=credentials["CONSUMER_SECRET"],
    access_token=credentials["ACCESS_TOKEN"],
    access_secret=credentials["ACCESS_SECRET"],
)

tweet_post = {"text": "hello world!"}

# create tweet:
c_resp = tweet(
    action=TweetAction.POST,
    data=tweet_post,
    auth=user_auth,
)

# Now check your twitter account!

# delete tweet:
tweet_id = c_resp["data"]["id"]
d_resp = tweet(
    action=TweetAction.DELETE,
    id=tweet_id,
    auth=user_auth,
)

# Now check your twitter account!
