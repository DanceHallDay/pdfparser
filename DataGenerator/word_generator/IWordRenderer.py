from abc import ABC
from DataGenerator.word_generator.IFont import IFont
from DataGenerator.word_generator.IVisualAugmenter import IVisualAugmenter
import numpy as np
from typing import List, Tuple
from PIL import ImageFont, Image, ImageDraw


class IWordRenderer(ABC):
    def word_render(
            self,
            word: str,
            font: IFont,
            font_size: int,
            augmenters: List[IVisualAugmenter],
            *args,
            **kwargs
    ) -> Tuple[np.array, str, List[int], List[int]]:
        """
        Renders @word into numpy array with shape (h,w) and dtype=uint8.
        Applies @augmenters to the generated image.
        Returns augmented image, word, x-coordinate of the start of each word's letter,
        and x-coordinate of the end of each word's letter
        """
        font_name = font.get_font_name()

        font = ImageFont.truetype(
            font=font_name,
            size=font_size
        )

        left, top, right, bottom = font.getbbox(word)
        width = right - left
        height = top - bottom

        img = Image.new('RGBA', (width, height), (255, 255, 255))
        img_draw = ImageDraw.Draw(img)
        img_draw.text((-left, -top), word, (0, 0, 0), font=font)

        lefts_x = []
        rights_x = []

        for i, char in enumerate(word):
            right_x,_ = font.getlength(word[:i + 1])
            width_char, _ = font.getmask(char).size

            right_x += left
            left_x = right_x - width_char

            lefts_x.append(left_x)
            rights_x.append(right_x)

        for augmenter in augmenters:
            img_draw = augmenter.augment(img_draw)

        return (np.array(img,dtype='uint8'), word, lefts_x, rights_x)
