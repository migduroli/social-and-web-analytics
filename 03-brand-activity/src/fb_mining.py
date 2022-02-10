#!/usr/bin/env python

import datetime
import json
import os
import re
import nltk

import facebook_scraper as fb
import logging
import pymongo as pymdb

logging.basicConfig(level=logging.INFO)


default_config = {
    "cookies_path": "auth/private/fb_cookies.json",
    "extract_options": {
        "comments": True,
        "allow_extra_requests": True,
        "progress": True,
        "reactors": True
    },
    "db_params": {
        "host": "localhost:27017",
        "collection": "scraping",
    },
    "max_pages": 100_000,
}


class FBScraper:

    @staticmethod
    def read_json_file(file):
        with open(file, "r") as input_file:
            return json.load(input_file)

    def _read_cookies(self):
        return self.read_json_file(file=self.cookies_path)

    def _set_cookies(self):
        self.fb.set_cookies(self.cookies)

    def _initialise_mongo(self):
        self.db_client = pymdb.MongoClient(self.db_params["host"])
        self.collection = self.db_client[self.db_params["collection"]]

    def _write_post_db(self, post: dict, database: str):
        post_id = post.pop("post_id")
        record = {**post, "_id": post_id}
        self.database = self.collection[database]
        try:
            self.database.insert_one(record)
            logging.info(f"Post inserted: {post_id}")
        except pymdb.errors.DuplicateKeyError:
            logging.info(f"{post_id} is already in our DB: Updating record")
            self.database.update_one(
                {"_id": post_id},
                {"$set": record}
            )

    def __init__(
            self,
            extract_options: dict,
            db_params: dict,
            max_pages: int = None,
            cookies_path: str = None,
    ):
        self.fb = fb

        if cookies_path:
            self.cookies_path = cookies_path
            self.cookies = self._read_cookies()
            self._set_cookies()

        self.options = extract_options
        self.max_pages = max_pages

        self.db_params = db_params
        self._initialise_mongo()

    def mine_posts(self, account):
        posts_iterator = self.fb.get_posts(
            account=account,
            options=self.options,
            extra_info=True,
            pages=self.max_pages
        )

        posts = []
        for post in posts_iterator:
            self._write_post_db(post, database=account)
            posts += []

        return posts

    def read_posts(self, account, limit=100):
        collection = self.collection[account]
        cursor = collection.find({})
        if limit:
            cursor = cursor.limit(limit)

        posts = []
        for document in cursor:
            posts += [document]

        return posts


def mine_posts(account: str, config=None):
    if config is None:
        config = default_config

    my_scraper = FBScraper(**config)
    my_scraper.mine_posts(account=account)


def read_posts(account: str, config=None, limit=100):
    if config is None:
        config = default_config

    fb = FBScraper(**config)
    return fb.read_posts(account=account, limit=limit)


if __name__ == "__main__":
    mine_posts("CocaColaEsp")
