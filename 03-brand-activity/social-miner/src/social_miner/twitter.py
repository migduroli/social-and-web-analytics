#!/usr/bin/env python

import argparse
import json
import logging
import tweepy

import pymongo as pymdb

from enum import Enum
from social_miner.commons import FileFormat, dump_binary_pickle


logging.basicConfig(level=logging.INFO)


class APIScraper:

    DEFAULT_DB_CONFIG = {
        "host": "localhost:27017",
        "collection": "twitter",
    }

    MAX_ITEMS = 100_000

    @staticmethod
    def read_json_file(file):
        with open(file, "r") as input_file:
            return json.load(input_file)

    def _read_credentials(self):
        return self.read_json_file(file=self.credentials_file)

    def _initialise_mongo(self):
        self.db_client = pymdb.MongoClient(self.db_params["host"])
        self.collection = self.db_client[self.db_params["collection"]]

    def _initialise_api_client(self):
        pass

    def _initialise_api(self):
        self._initialise_api_client()

    def _save_post(self, post_id: str, post: dict, database: str):
        record = {**post, "_id": post_id}
        self.database = self.collection[database]
        try:
            self.database.insert_one(record)
            logging.info(f"Post inserted: {self.collection.name}:{database}.{post_id}")
        except pymdb.errors.DuplicateKeyError:
            logging.info(f"{self.collection.name}:{database}.{post_id} is already in our DB: Updating record")
            self.database.update_one(
                {"_id": post_id},
                {"$set": record}
            )

    def __init__(
            self,
            credentials_path: str,
            db_params: dict,
            max_pages: int = None,
            max_items: int = None,
            extract_options: dict = None,
    ):
        self.credentials_file = credentials_path
        self.credentials = self._read_credentials()

        self.api = None
        self._initialise_api()

        self.options = extract_options
        self.max_pages = max_pages
        self.max_results = max_items

        self.db_params = db_params
        self._initialise_mongo()


class TwitterVersion(Enum):
    V1 = 1
    V2 = 2


class TwitterScraper(APIScraper):

    API_VERSION_ERROR_MSG = "The version specified {version} is not yet available..."
    DEFAULT_TWEET_FIELDS = [
        "id", "text", "created_at", "public_metrics", "referenced_tweets",
    ]

    def _initialise_api_client(self):
        auth = tweepy.OAuthHandler(
            self.credentials["CONSUMER_KEY"],
            self.credentials["CONSUMER_SECRET"]
        )
        auth.set_access_token(
            self.credentials["ACCESS_TOKEN"],
            self.credentials["ACCESS_SECRET"],
        )

        if self.api_version == TwitterVersion.V1:
            self.api = tweepy.API(
                auth=auth,
                wait_on_rate_limit=True,
            )

        elif self.api_version == TwitterVersion.V2:
            credentials = self.credentials
            self.api = tweepy.Client(
                bearer_token=credentials["BEARER_TOKEN"],
                consumer_key=credentials["CONSUMER_KEY"],
                consumer_secret=credentials["CONSUMER_SECRET"],
                access_token=credentials["ACCESS_TOKEN"],
                access_token_secret=credentials["ACCESS_SECRET"],
                wait_on_rate_limit=True,
            )

        else:
            raise NotImplementedError(
                self.API_VERSION_ERROR_MSG.format(version=self.api_version)
            )

    def _get_iterator(self, func, kwargs):

        if self.api_version == TwitterVersion.V2:
            return tweepy.Paginator(
                func,
                **kwargs,
                max_results=self.max_results
            ).flatten(limit=self.max_results)

        elif self.api_version == TwitterVersion.V1:
            return tweepy.Cursor(
                func,
                **kwargs,
                count=self.max_results
            ).pages(self.max_pages)

        else:
            raise NotImplementedError(
                self.API_VERSION_ERROR_MSG.format(version=self.api_version)
            )

    def _get_user_tweets(self, user_name=None, user_id=None, **kwargs):
        if not user_id:
            user = self.api.get_user(
                username=user_name,
                user_fields=["id", "public_metrics"]
            ).data
            user_id = user.id

        iterator = tweepy.Paginator(
            self.api.get_users_tweets,
            id=user_id,
            **kwargs,
        ).flatten(limit=self.max_results)

        return user, iterator

    def mine_user_tweets(self, user_name=None, user_id=None, **kwargs):
        if "tweet_fields" not in kwargs.keys():
            kwargs["tweet_fields"] = self.tweet_fields

        tweets = []
        user, tweets_iterator = self._get_user_tweets(
            user_name=user_name,
            user_id=user_id,
            **kwargs
        )

        for t in tweets_iterator:
            ret_objs = self.api.get_retweeters(
                id=t.id,
                user_fields=[
                    "id",
                    "name",
                    "username",
                    "description",
                    "entities",
                    "verified",
                    "public_metrics",
                ]
            ).data
            try:
                retweeters = [dict(rt) for rt in ret_objs]
            except:
                retweeters = []

            record = dict(t)
            record = {
                **record,
                "user_metrics": user.public_metrics,
                "retweeters": retweeters
            }
            self._save_post(
                post_id=t.id,
                post=record,
                database=user_name
            )
            tweets.append(t)
        return tweets

    def __init__(
            self,
            credentials_path: str,
            db_params: dict,
            api_version: TwitterVersion = TwitterVersion.V2,
            max_pages: int = None,
            max_items: int = None,
            extract_options: dict = None,
            tweet_fields=None
    ):
        if tweet_fields is None:
            tweet_fields = TwitterScraper.DEFAULT_TWEET_FIELDS

        self.api_version = api_version
        if self.api_version == TwitterVersion.V1:
            logging.warning(self.API_VERSION_ERROR_MSG)

        super().__init__(
            credentials_path,
            db_params,
            max_pages,
            max_items,
            extract_options,
        )

        self.tweet_fields = tweet_fields

    def read_tweets(self, user_name, limit=100):
        collection = self.collection[user_name]
        cursor = collection.find({})
        if limit:
            cursor = cursor.limit(limit)

        posts = []
        for document in cursor:
            posts += [document]

        return posts

    def dump_tweets(
            self,
            user_name: str,
            limit=None,
            file_format: FileFormat = FileFormat.PICKLE
    ):
        collection = self.collection[user_name]
        cursor = collection.find({})
        if limit:
            cursor = cursor.limit(limit)

        logging.info(f"Dumping collection {user_name}...")
        filename = f"tw_tweets_{user_name}." + file_format.name.lower()

        counter = dump_binary_pickle(cursor, filename)

        logging.info(f"Total collection records: {counter}")
        logging.info(f"Collection {user_name} dumped in {filename}")
        return


def mine_tweets(
        account: str,
        limit: int = 100,
        credentials_path: str = "auth/private/twitter_credentials.json",
        db_params=None
):
    if db_params is None:
        db_params = APIScraper.DEFAULT_DB_CONFIG

    tw = TwitterScraper(
        credentials_path=credentials_path,
        db_params=db_params,
        api_version=TwitterVersion.V2,
        max_items=limit,
    )

    return tw.mine_user_tweets(user_name=account)


def read_tweets(
        account: str,
        limit: int = 100,
        credentials_path: str = "auth/private/twitter_credentials.json",
        db_params=None
):
    if db_params is None:
        db_params = APIScraper.DEFAULT_DB_CONFIG

    tw = TwitterScraper(
        credentials_path=credentials_path,
        db_params=db_params,
        api_version=TwitterVersion.V2,
        max_items=limit,
    )

    return tw.read_tweets(user_name=account, limit=limit)


def dump_tweets(
        account: str,
        limit: int = None,
        credentials_path: str = "auth/private/twitter_credentials.json",
        db_params=None,
        file_format: FileFormat = FileFormat.PICKLE
):
    if db_params is None:
        db_params = APIScraper.DEFAULT_DB_CONFIG

    tw = TwitterScraper(
        credentials_path=credentials_path,
        db_params=db_params,
        api_version=TwitterVersion.V2,
        max_items=limit,
    )

    return tw.dump_tweets(user_name=account, limit=limit, file_format=file_format)


def mine_tweets_console(
        db_params=None,
        limit: int = None,
):
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("-c", "--credentials", required=True)
    args = parser.parse_args()

    if db_params is None:
        db_params = APIScraper.DEFAULT_DB_CONFIG
    if not limit:
        limit = APIScraper.MAX_ITEMS

    tw = TwitterScraper(
        credentials_path=args.credentials,
        db_params=db_params,
        api_version=TwitterVersion.V2,
        max_items=limit,
    )

    tw.mine_user_tweets(user_name=args.username)


if __name__ == "__main__":
    mine_tweets_console()

