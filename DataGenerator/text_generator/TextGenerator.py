from DataGenerator.text_generator.ITextGenerator import ITextGenerator
from DataGenerator.word_generator.IFont import IFont
from DataGenerator.word_generator.IVisualAugmenter import IVisualAugmenter
from DataGenerator.word_generator.IWordGenerator import IWordGenerator
from DataGenerator.word_generator.IWordRenderer import IWordRenderer
import numpy as np
from typing import List, Tuple


class TextGenerator(ITextGenerator):
    def __init__(
        self,
        fonts: Tuple[List[IFont], np.array],
        font_sizes: Tuple[List[int], np.array],
        augmenters: List[IVisualAugmenter],
        word_generator: IWordGenerator,
        word_renderer: IWordRenderer,
        *args,
        **kwargs
    ) -> None:
        self.fonts = fonts
        self.font_sizes = font_sizes
        self.augmenters = augmenters
        self.word_generator = word_generator
        self.word_renderer = word_renderer

    def generate(self, n: int) -> List[str, IWordRenderer.word_render]:
        return [
            self.word_renderer.word_render(
                self.word_generator.word_generate(1),
                np.random.choice(self.fonts[0], p=self.fonts[1]),
                np.random.choice(self.font_sizes[0], p=self.font_sizes[1]),
                self.augmenters,
            )
            for _ in range(n)
        ]
