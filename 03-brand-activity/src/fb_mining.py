import datetime
import json
import os
import re
import nltk

import facebook_scraper as fb
import pandas as pd
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


posts = read_posts("Google")
posts_cols = [
    '_id', 'text', 'post_text', 'shared_text', 'time', 'video_watches',
    'likes', 'comments', 'shares', 'user_id',
]

comments_cols = [
    '_id', 'comments_full',
]

comments_data = [{k: p[k] for k in comments_cols} for p in posts]
posts_data = [{k: p[k] for k in posts_cols} for p in posts]

posts_df = pd.DataFrame(posts_data).rename(
    columns={"_id": "id"}
)

comments_full_cols = [
    "id",
    "comment_time",
    "comment_text",
    "comment_reactions",
]
comments_df = pd.DataFrame(
    columns=comments_full_cols
)
for c in comments_data:
    c_df = pd.json_normalize(c["comments_full"])
    try:
        c_df.loc[:, "id"] = c["_id"]
        comments_df = comments_df.append(
            c_df[comments_full_cols]
        )
    except:
        print(f"Unable to insert: {c['_id']} ({c_df.shape})")


comments_df = pd.DataFrame(
    columns=comments_full_cols
)


# Preprocess:
def preprocess(text: str):
    # cleans white spaces and punctuation, and converts text to lower
    c_text = re.sub(
        pattern=r"[^\w\s]",
        repl="",
        string=text.lower().strip()
    )

    # tokenize words:
    tokens = nltk.word_tokenize(c_text)
    return tokens


# Feature extraction:
def get_hashtags(text):
    hashtags = re.findall(
        pattern=r"#(\w+)",
        string=text
    )
    return hashtags


# Syntax:
def tag_tokens(text):
    # Get the part-of-speech of a word in a sentence:
    pos = nltk.pos_tag(text)
    return pos


#
def get_keywords(tagged_tokens, pos="all"):
    if pos == "all":
        lst_pos = ("NN", "JJ", "VP")
    elif pos == "nouns":
        lst_pos = "NN"
    elif pos == "verbs":
        lst_pos = "VB"
    elif pos == "adjectives":
        lst_pos = "JJ"
    else:
        lst_pos = ("NN", "JJ", "VP")

    keywords = [
        t[0] for t in tagged_tokens if t[1].startswith(lst_pos)
    ]
    return keywords


# Get noun phrases:
def get_noun_phrases(tagged_tokens):
    # Optional determiner, and multiple adjts and nouns
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(tagged_tokens)

    result = []

    def is_noun(token):
        return token.label() == "NP"

    for subtree in tree.subtrees(filter = is_noun):
        leaves = subtree.leaves()
        if len(leaves) > 1:
            outputs = " ".join([
                t[0] for t in leaves
            ])
            result += [outputs]

    return result


def execute_pipeline(df, msg_col="post_text"):
    df["hastags"] = df.apply(
        lambda x: get_hashtags(x[msg_col]),
        axis=1
    )
    df["preprocessed"] = df.apply(
        lambda x: preprocess(x[msg_col]),
        axis=1
    )
    df["tagged"] = df.apply(
        lambda x: tag_tokens(x["preprocessed"]),
        axis=1
    )
    df["keywords"] = df.apply(
        lambda x: get_keywords(x["tagged"]),
        axis=1
    )
    df["noun_phrases"] = df.apply(
        lambda x: get_noun_phrases(x["tagged"]),
        axis=1
    )

    return df