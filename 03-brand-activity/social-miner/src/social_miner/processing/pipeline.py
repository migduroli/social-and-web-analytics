import itertools

import pandas as pd
import nltk
import re

import wordcloud as wc

import matplotlib.pyplot as plt


# Feature extraction:
def extract_hashtags(text):
    hashtags = list(set(re.findall(
        pattern=r"#(\w+)",
        string=text
    )))
    return hashtags


def remove_urls(text: str):
    # remove all URLs inside a string:
    return re.sub(
        r"^https?:\/\/.*[\r\n]*", "", text, flags=re.MULTILINE
    )


# Preprocess:
def preprocess_and_tokenize(text: str, filter_urls: bool = True):
    # cleans white spaces and punctuation, and converts text to lower
    c_text = re.sub(
            pattern=r"[^\w\s]",
            repl="",
            string=text.lower().strip()
        )

    if filter_urls:
        c_text = remove_urls(c_text)

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
        figsize=(20, 10),
        collocations=False,
        noise_words=NOISE_WORDS,
        black_and_white=False,
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
        max_words=500,
        max_font_size=80,
        random_state=50,
        width=width,
        height=height,
        collocations=collocations,
        font_path='/Library/Fonts/Arial Unicode.ttf',
    ).generate_from_text(" ".join(phrases))

    if black_and_white:
        def black_color_func(
                word,
                font_size,
                position,
                orientation,
                random_state=None,
                **kwargs):
            return "hsl(0,100%, 1%)"
        res.recolor(color_func=black_color_func)

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