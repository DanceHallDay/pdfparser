from abc import ABC
from DataGenerator.word_generator.IFont import IFont
from DataGenerator.word_generator.IVisualAugmenter import IVisualAugmenter
import numpy as np
from typing import List, Tuple


class IWordRenderer(ABC):
    def word_render(
        self, word: str, font: IFont, font_size: int, *args, **kwargs
    ) -> Tuple[np.array, str, np.array, np.array]:
        """
        Renders @word into numpy array with shape (h,w) and dtype=uint8.
        Returns image, word, x-coordinate of the start of each word's letter,
        and x-coordinate of the end of each word's letter
        """
        pass
