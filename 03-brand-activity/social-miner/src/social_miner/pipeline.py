import itertools

import pandas as pd
import nltk
import re

import wordcloud as wc

import matplotlib.pyplot as plt

# posts = list()
#
# posts_cols = [
#     '_id', 'text', 'post_text', 'shared_text', 'time', 'video_watches',
#     'likes', 'comments', 'shares', 'user_id',
# ]
#
# comments_cols = [
#     '_id', 'comments_full',
# ]
#
# comments_data = [{k: p[k] for k in comments_cols} for p in posts]
# posts_data = [{k: p[k] for k in posts_cols} for p in posts]
#
# posts_df = pd.DataFrame(posts_data).rename(
#     columns={"_id": "id"}
# )
#
# comments_full_cols = [
#     "id",
#     "comment_time",
#     "comment_text",
#     "comment_reactions",
# ]
# comments_df = pd.DataFrame(
#     columns=comments_full_cols
# )
# for c in comments_data:
#     c_df = pd.json_normalize(c["comments_full"])
#     try:
#         c_df.loc[:, "id"] = c["_id"]
#         comments_df = comments_df.append(
#             c_df[comments_full_cols]
#         )
#     except:
#         print(f"Unable to insert: {c['_id']} ({c_df.shape})")
#
#
# comments_df = pd.DataFrame(
#     columns=comments_full_cols
# )


# Feature extraction:
def extract_hashtags(text):
    hashtags = list(set(re.findall(
        pattern=r"#(\w+)",
        string=text
    )))
    return hashtags


# Preprocess:
def preprocess_and_tokenize(text: str):
    # cleans white spaces and punctuation, and converts text to lower
    c_text = re.sub(
        pattern=r"[^\w\s]",
        repl="",
        string=text.lower().strip()
    )

    # tokenize words:
    tokens = nltk.word_tokenize(c_text)
    return tokens


# Syntax:
def tag_tokens(text):
    # Get the part-of-speech of a word in a sentence:
    pos = nltk.pos_tag(text)
    return pos


#
def extract_keywords(tagged_tokens, pos="all"):
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
def extract_noun_phrases(tagged_tokens):
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


def processing_pipeline(df, msg_col):
    df["hastags"] = df.apply(
        lambda x: extract_hashtags(x[msg_col]),
        axis=1
    )
    df["preprocessed"] = df.apply(
        lambda x: preprocess_and_tokenize(x[msg_col]),
        axis=1
    )
    df["tagged"] = df.apply(
        lambda x: tag_tokens(x["preprocessed"]),
        axis=1
    )
    df["keywords"] = df.apply(
        lambda x: extract_keywords(x["tagged"]),
        axis=1
    )
    df["noun_phrases"] = df.apply(
        lambda x: extract_noun_phrases(x["tagged"]),
        axis=1
    )

    return df


NOISE_WORDS = []


def generate_wordcloud(
        df: pd.DataFrame, col,
        width=800,
        height=400,
        figsize=(20,10),
        collocations=False,
        noise_words=NOISE_WORDS,
):
    tokens = list(
        itertools.chain.from_iterable(df[col])
    )

    phrases = [
        phrase.replace(" ", "_") for phrase in tokens
        if len(phrase) > 1
    ]

    phrases = [
        p for p in phrases if not any(spam in p.lower() for spam in NOISE_WORDS)
    ]

    res = wc.WordCloud(
        background_color="white",
        max_words=2_000,
        max_font_size=80,
        random_state=50,
        width=width,
        height=height,
        collocations=collocations,
    ).generate(" ".join(phrases))

    plt.figure(figsize=figsize)
    plt.imshow(res)
    plt.axis("off")
    plt.show()

    return res


def get_verbatims(
        df: pd.DataFrame,
        keyword: str,
        text_col: str,
        n: int = 100,
):
    sub_df = df[
        df[text_col].str.contains(keyword)
    ]

    verbatims = [
        r[text_col]
        for idx, r in sub_df.head(n).iterrows()
    ]

    return verbatims