from abc import ABC
from typing import List


class IWordGenerator(ABC):
    def word_generate(self, text_space: List[str], case: int, *args, **kwargs) -> str:
        """
        generate random a word from @text_space with a specific formatting,
        that is setted by @case variable:
        case:
            1 - generate low case
            2 - generate uppercase
            3 - generate capitalized
        """
        pass

    def word_storage_load(self, path: str, vocab: str, *args, **kwargs) -> None:
        """
        Loads words from a file that is specified by @path.
        filter all words with @vocab.
        creates internally list of words from the file
        """
        pass
