import os
import math
import nltk
import re
import pandas as pd

from typing import List
from enum import Enum


class PennTreebank(Enum):
    CC = 1  # Coordinating conjunction
    CD = 2  # Cardinal number
    DT = 3  # Determiner
    EX = 4  # Existential there
    FW = 5  # Foreign word
    IN = 6  # Preposition or subordinating conjunction
    JJ = 7  # Adjective
    JJR = 8  # Adjective, comparative
    JJS = 9  # Adjective, superlative
    LS = 10  # List item marker
    MD = 11  # Modal
    NN = 12  # Noun, singular or mass
    NNS = 13  # Noun, plural
    NNP = 14  # Proper noun, singular
    NNPS = 15  # Proper noun, plural
    PDT = 16  # Predeterminer
    POS = 17  # Possessive ending
    PRP = 18  # Personal pronoun
    # PRP$ = 19 # Possessive pronoun
    RB = 20  # Adverb
    RBR = 21  # Adverb, comparative
    RBS = 22  # Adverb, superlative
    RP = 23  # Particle
    SYM = 24  # Symbol
    TO = 25  # to
    UH = 26  # Interjection
    VB = 27  # Verb, base form
    VBD = 28  # Verb, past tense
    VBG = 29  # Verb, gerund or present participle
    VBN = 30  # Verb, past participle
    VBP = 31  # Verb, non-3rd person singular present
    VBZ = 32  # Verb, 3rd person singular present
    WDT = 33  # Wh-determiner
    WP = 34  # Wh-pronoun
    # WP$ = 35 # Possessive wh-pronoun
    WRB = 36  # Wh-adverb


class SentimentOrientation:
    Positive = "pos"
    Negative = "neg"


class ReferenceWords:
    highly_positive = "great"
    highly_negative = "poor"


def read_document(filename: str) -> str:
    with open(filename, "r", encoding="utf8") as file:
        return file.read()


def build_train_test_per_fold(
        datasets: list,
        classes: List[str],
        data_path: str,
        filenames: dict,
        fold: int,
        max_train_files: int = None,
        max_test_files: int = None,
) -> list:
    trains = {c: [] for c in classes}
    tests = {c: [] for c in classes}

    for c in classes:
        for filename in filenames[c]:
            file_path = f"{data_path}/{c}/{filename}"

            if filename[2] == str(fold):
                tests[c].append(file_path)
                trains[c].append(file_path)
            else:
                trains[c].append(file_path)

    max_trains = len(trains.items()) \
        if not max_train_files \
        else max_train_files

    max_tests = len(tests.items()) \
        if not max_test_files \
        else max_test_files

    datasets.append({
        'train': {
            c: d[:max_trains] for (c, d) in trains.items()
        },
        'test': {
            c: d[:max_tests] for (c, d) in tests.items()
        }
    })

    return datasets


def prepare_datasets(
        data_path: str,
        n_folds: int = 1,
        max_train_files: int = None,
        max_test_files: int = None,
):
    classes = os.listdir(data_path)
    filenames = {
        c: sorted(os.listdir(f"{data_path}/{c}/"))
        for c in classes
    }

    datasets = []
    for fold in range(n_folds):
        build_train_test_per_fold(
            datasets=datasets,
            classes=classes,
            data_path=data_path,
            filenames=filenames,
            fold=fold,
            max_train_files=max_train_files,
            max_test_files=max_test_files,
        )

    return datasets


def append_tag_pattern(
        condition: bool,
        tag_pattern: list,
        first_word: list,
        second_word: list,
) -> list:
    if condition:
        tag_pattern.append(
            "".join(first_word) + " " + "".join(second_word)
        )
        return tag_pattern


def check_turney_patterns(
        postag_1,
        postag_2,
        postag_3,
):
    patterns = []

    patterns.append(
        postag_1[1] in [PennTreebank.JJ.name] and
        (postag_2[1] in [PennTreebank.NN.name, PennTreebank.NNS.name])
    )

    patterns.append(
        (postag_1[1] in [
            PennTreebank.RB.name,
            PennTreebank.RBR.name,
            PennTreebank.RBS.name,
            PennTreebank.JJ.name,
            PennTreebank.NN.name,
            PennTreebank.NNS.name,
        ]) and (postag_2[1] in [PennTreebank.JJ.name] and
                postag_3[1] not in [
                            PennTreebank.NN.name,
                            PennTreebank.NNS.name
                        ])
    )

    patterns.append(
        (postag_1[1] in [
            PennTreebank.RB.name,
            PennTreebank.RBR.name,
            PennTreebank.RBS.name
        ]) and (postag_2[1] in [
            PennTreebank.VB.name,
            PennTreebank.VBD.name,
            PennTreebank.VBN.name,
            PennTreebank.VBG.name
        ])
    )

    return any(patterns)


def find_pattern(postag):
    tag_pattern = []
    for k in range(len(postag) - 2):
        append_tag_pattern(
            condition=check_turney_patterns(
                postag_1=postag[k],
                postag_2=postag[k + 1],
                postag_3=postag[k + 2],
            ),
            tag_pattern=tag_pattern,
            first_word=postag[k][0],
            second_word=postag[k + 1][0],
        )
    return tag_pattern


def near_operator(phrase, word, text):
    try:
        string = word + r'\W+(?:\w+\W+){0,500}?' + phrase + r'|' \
                 + phrase + r'\W+(?:\w+\W+){0,500}?' + word
        freq_phrase_near_word = (len(re.findall(string, text)))
        return freq_phrase_near_word
    except:
        return 0


class Turney(object):

    def __init__(
            self,
            datasets,
            positive_hits_init: float = 0.01,
            negative_hits_init: float = 0.01,
            positive_tag: str = SentimentOrientation.Positive,
            negative_tag: str = SentimentOrientation.Negative,
            positive_word: str = ReferenceWords.highly_positive,
            negative_word: str = ReferenceWords.highly_negative,
            n_folds: int = 1,
    ):
        self.datasets = datasets
        self.pos_phrases_hits = []
        self.neg_phrases_hits = []
        self.pos_hits = positive_hits_init
        self.neg_hits = negative_hits_init
        self.pos_hits_init = positive_hits_init
        self.neg_hits_init = negative_hits_init
        self.sentiments = {}
        self.confusion_matrix = pd.DataFrame({
            "ActualPos": [0, 0],
            "ActualNeg": [0, 0],
        }, index=["PredPos", "PredNeg"])

        self._positive_tag = positive_tag
        self._negative_tag = negative_tag

        self._classes = [
            self._positive_tag,
            self._negative_tag
        ]

        self._positive_word = positive_word
        self._negative_word = negative_word

        self._n_folds = n_folds

    def _compute_hits(self, phrases: list, n_fold: int = 0):
        self.pos_phrases_hits = [self.pos_hits_init] * len(phrases)
        self.neg_phrases_hits = [self.neg_hits_init] * len(phrases)
        self.pos_hits = self.pos_hits_init
        self.neg_hits = self.neg_hits_init

        for train_klass in self._classes:
            for k, file in enumerate(self.datasets[n_fold]['train'][train_klass]):
                txt_file = read_document(file)
                for ind, phrase in enumerate(phrases):
                    self.pos_phrases_hits[ind] += near_operator(
                        phrase=phrase,
                        word=self._positive_word,
                        text=txt_file
                    )
                    self.neg_phrases_hits[ind] += near_operator(
                        phrase=phrase,
                        word=self._negative_word,
                        text=txt_file
                    )
                    self.pos_hits += txt_file.count(self._positive_word)
                    self.neg_hits += txt_file.count(self._negative_word)

    def evaluate(self):
        n_fold = 0
        for test_klass in self._classes:
            for i, data in enumerate(self.datasets[n_fold]['test'][test_klass]):
                print(f"{test_klass.title()} Document: {i}")
                text = read_document(data)

                doc_tokens = find_pattern(
                    postag=nltk.pos_tag(nltk.word_tokenize(text))
                )

                self._compute_hits(doc_tokens)

                so = self.compute_sentiment_orientation()

                is_negative = (test_klass == self._negative_tag)
                self._update_confusion_matrix(
                    predict=so,
                    is_negative=is_negative
                )

                self.sentiments.update({
                    data: so
                })
                print(f"\tPredicted = {so} ({'pos' if so > 0 else 'neg'}) |"
                      f" Actual = {test_klass}")

        print("Final Confusion Matrix")
        print(self.confusion_matrix)

    def compute_sentiment_orientation(self):
        polarities = [
            math.log((self.pos_phrases_hits[i] * self.neg_hits) /
                     (self.neg_phrases_hits[i] * self.pos_hits), 2)
            for i in range(len(self.pos_phrases_hits))
        ]

        so = sum(polarities) / len(polarities)
        return so

    def _update_confusion_matrix(self, predict, is_negative: bool):
        if predict > 0 and (not is_negative):
            self.confusion_matrix.loc["PredPos", "ActualPos"] += 1
        if predict < 0 and is_negative:
            self.confusion_matrix.loc["PredNeg", "ActualNeg"] += 1
        if predict > 0 and is_negative:
            self.confusion_matrix.loc["PredPos", "ActualNeg"] += 1
        if predict < 0 and not is_negative:
            self.confusion_matrix.loc["PredNeg", "ActualPos"] += 1