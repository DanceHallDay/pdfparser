from ITextGenerator import *

class TextGenerator(ITextGenerator):
    def initialize(
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

    def generate(self, n: int) -> List[IWordRenderer.word_render]:
        return [
            self.word_renderer.word_render(
                self.word_generator.word_generate(),
                np.random.choice(self.fonts[0], p=self.fonts[1]),
                np.random.choice(self.font_sizes[0], p=self.font_sizes[1]),
                self.augmenters
            )
            for _ in range(n)
        ]
