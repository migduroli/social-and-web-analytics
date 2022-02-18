import pickle
from enum import Enum


class FileFormat(Enum):
    JSON = 0
    BSON = 1
    PICKLE = 2


def dump_binary_pickle(cursor, filename: str):
    file = open(filename, "wb+")
    counter = 0
    for doc in cursor:
        pickle.dump(doc, file)
        counter += 1
    return counter


def load_binary_pickle(filename: str):
    objects = []
    with open(filename, "rb") as file:
        while True:
            try:
                objects.append(pickle.load(file))
            except EOFError:
                break
    return objects
