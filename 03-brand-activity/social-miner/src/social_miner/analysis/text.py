import itertools
import pandas as pd
import wordcloud as wc
import matplotlib.pyplot as plt


def generate_wordcloud(
        df: pd.DataFrame, col,
        width=800,
        height=400,
        figsize=(20, 10),
        collocations=False,
        noise_words=None,
        black_and_white=False,
):
    if noise_words is None:
        noise_words = []

    tokens = list(
        itertools.chain.from_iterable(df[col])
    )

    phrases = [
        phrase.replace(" ", "_") for phrase in tokens
        if len(phrase) > 1
    ]

    phrases = [
        p for p in phrases if not any(spam in p.lower() for spam in noise_words)
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
