from IWordRenderer import *
from PIL import ImageFont, Image, ImageDraw


class WordRenderer(IWordRenderer):

    def word_render(
            self,
            word: str,
            font: IFont,
            font_size: int,
            augmenters: List[IVisualAugmenter],
            *args,
            **kwargs
    ) -> Tuple[np.array, str, List[int], List[int]]:

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

        starts_x = []
        ends_x = []

        for i, char in enumerate(word):
            end_x, _ = font.getsize(word[:i + 1])
            width_char, _ = font.getmask(char).size

            end_x += left
            start_x = end_x - width_char

            starts_x.append(start_x)
            ends_x.append(end_x)

        img_arr = np.array(img, dtype='uint8')

        for augmenter in augmenters:
            img_arr, starts_x, ends_x = augmenter.augment(img_arr, starts_x=starts_x, ends_x=ends_x)

        return img_arr, word, starts_x, ends_x
