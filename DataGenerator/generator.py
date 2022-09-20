from DataGenerator.word_generator.WordGenerator import WordGenerator
from DataGenerator.word_generator.WordRenderer import WordRenderer
from DataGenerator.word_generator.Font import Font
from DataGenerator.word_generator.VisualAugmenter import (
    VisualAugmenterRotation,
    VisualAugmenterGaussianNoise,
    VisualAugmenterStretching,
    VisualAugmenterErosion,
    VisualAugmenterDilation,
)
from DataGenerator.text_generator.TextGenerator import TextGenerator
from DataGenerator.const import VOCABS

import numpy as np
import matplotlib.pyplot as plt


def generate(font_path, wl_path, n):
    font = Font().load_font(font_path)

    word_generator = WordGenerator()
    word_generator.word_storage_load(wl_path, VOCABS["english"])

    word_renderer = WordRenderer()

    visual_augmenter_rotation = VisualAugmenterRotation(-1, 1)
    visual_augmenter_gauss = VisualAugmenterGaussianNoise(1, 1)
    visual_augmenter_stretching = VisualAugmenterStretching([0.1, 0.2], [0.3, 0.5])

    text_generator = TextGenerator(
        ([font], [1]),
        ([10, 20], [0.5, 0.5]),
        [visual_augmenter_rotation],
        word_generator,
        word_renderer,
    )

    samples = text_generator.generate(n)

    return samples


if __name__ == "__main__":
    font_path = "fonts/Arial_Bold.ttf"
    wl_path = "word_storage/eng_30k.wl"

    samples_count = 10
    samples = generate(font_path, wl_path, samples_count)

    for s in samples:
        img, word, x_start, x_end = s
        print(word, x_start, x_end)

    plt.imshow(samples[0][0])
    plt.show()


