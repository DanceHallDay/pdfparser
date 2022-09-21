import pandas as pd
import itertools
from DataGenerator.word_storage.utils import filter_uniq, save_words


def fetch_words(row, key):
    rows = row[key].split()
    return rows


def concat(seq):
    res = itertools.chain(*seq)
    return res


if __name__ == "__main__":
    path_train = "JEOPARDY_QUESTIONS1.json"

    df = pd.read_json(path_train)
    # Index(['category', 'air_date', 'question', 'value', 'answer', 'round',
    #    'show_number'],

    text_list_q = df["question"].to_list()
    text_list_a = df["answer"].to_list()

    text_list = text_list_q + text_list_a

    text = " ".join(text_list)

    words = filter_uniq(text)

    print(len(words))

    save_words(words, "jeopardy.wl")
