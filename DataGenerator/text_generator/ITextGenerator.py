from abc import ABC
from DataGenerator.word_generator.IFont import IFont
from DataGenerator.word_generator.IVisualAugmenter import IVisualAugmenter
from DataGenerator.word_generator.IWordGenerator import IWordGenerator
from DataGenerator.word_generator.IWordRenderer import IWordRenderer
import numpy as np
from typing import List, Tuple, Union


class ITextGenerator(ABC):
    def __init__(
        self,
        fonts: Tuple[List[IFont], List[float]],
        font_sizes: Tuple[List[int], List[float]],
        word_generator: Tuple[IWordGenerator, List[float]],
        augmenters: List[IVisualAugmenter],
        word_renderer: IWordRenderer,
        *args,
        **kwargs
    ):
        """
        Set up generator settings.
        @fonts - tuple of fonts and their PDF fucntion,
        @font_sizes - tuple of fonts sizes and their PDF fucntion,
        @word_generator - tuple of IWordGenerator instance, it's case PDF (upper, low, capital),
        @augmenters - list of augmenters,
        @word_renderer - IWordRenderer instance
        """
        pass

    def generate(
        self, n: int
    ) -> Union[List[Tuple[IFont, IWordRenderer.word_render]], None]:
        """
        Generates list of tuples, each tuple is generated IFont and
        IWordRenderer.word_render function's output
        size of generated list equals aug_count * @n, and from 1 to aug_count * @n
        - if rest words is being generated, and None if there are no rest any words in IWordGenerator
        """
        pass
