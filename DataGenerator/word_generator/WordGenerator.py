from IWordGenerator import IWordGenerator
from typing import List
import re
import numpy as np
import os

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
        if not os.path.isfile(path) or not (path.lower().endswith('.wl') or path.lower().endswith('.txt')):
            raise OSError("only .wl and .txt fonts can be used")

        #replace all characters that aren't in the vocab with a character ''
        with open(path, "r") as f:
            self.__words.extend(
                [
                    re.sub(f"[^{vocab}]", "", word)
                    for line in f.readlines()
                    for word in line.split()
                    if re.sub(f"[^{vocab}]", "", word) != '' 
                ]
            )