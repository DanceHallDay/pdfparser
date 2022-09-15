from IWordGenerator import IWordGenerator
from typing import List
import re
import numpy as np

class WordGenerator(IWordGenerator):
    def __init__(self):
        self.__words = []

    def word_generate(self, case: int, *args, **kwargs) -> str:
        word = self.__words[np.random.randint(0, len(self.__words))]

        if case == 1:
            word = word.lower()
        elif case == 2:
            word = word.upper()
        elif case == 3:
            word = word.capitalize()

        return word

    def word_storage_load(self, path: str, vocab: str, *args, **kwargs) -> None:
        with open(path, "r") as f:
            self.__words.extend(
                [
                    re.sub(f"[^{vocab}]", "", word)
                    for line in f.readlines()
                    for word in line.split()
                ]
            )