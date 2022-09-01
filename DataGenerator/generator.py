from PIL import Image, ImageDraw, ImageFont
from random_word import Wordnik
import random
import os
import numpy as np
from typing import List, Optional, Tuple

class RenderedTextGenerator():
    def __init__(
            self,
            fonts_folder: str,
            fonttype: str,
            fontsize_range: Tuple[int, int],
            img_shape: Optional[Tuple[int, int]]=None,
            batch_size: int=1,
            textMinLength: int=1,
            textMaxLength: int=10,
        ):
        self.__text_generator = Wordnik()
        self.__text_generator_params = {
            "minLength": textMinLength,
            "maxLength": textMaxLength,
        }
        self.fonttype = fonttype
        self.img_shape = img_shape
        self.batch_size = batch_size
        self.fontsize_range = fontsize_range
        self.fontnames = self.__get_fontnames(fonts_folder)

    
    def __get_fontnames(self, fonts_folder: str) -> List[str]:
        return [f'{fonts_folder}/{fontname}' for fontname in os.listdir(fonts_folder)]

    def get_random_fontname(self) -> str:
        i = random.randint(0, len(self.fontnames) - 1)
        return self.fontnames[i]

    def get_random_fontsize(self) -> int:
        return random.randint(self.fontsize_range[0], self.fontsize_range[1])
    
    def get_fonttype(self, fontname: str) -> str:
        if self.fonttype == 'bold':
            return 1 if 'bold' in fontname.lower() else 0
        else:
            return 1 if 'italic' in fontname.lower() else 0

    def generate_word(self) -> str:
        return str(self.__text_generator.get_random_word(**self.__text_generator_params))
    

    def render_text(self, save_path: Optional[str]=None) -> Tuple[np.array, np.array]:
        img_arr, type_arr = [], []
        for i in range(self.batch_size):
            text = self.generate_word()

            fontname = self.get_random_fontname()
            fonttype = self.get_fonttype(fontname)

            font = ImageFont.truetype(
                font=fontname, 
                size=self.get_random_fontsize()
            )

            left, top, right, bottom = font.getbbox(text)
            width, height = right - left, bottom - top

            text_img = Image.new("RGBA", (width, height), (255,255,255))
            text_img_draw = ImageDraw.Draw(text_img)
            text_img_draw.text((-left, -top), text, (0,0,0), font=font)

            if self.img_shape:
                text_img = text_img.resize(self.img_shape)

            if save_path:
                text_img.save(save_path)
            
            img_arr.append(np.array(text_img))
            type_arr.append(fonttype)

        return np.array(img_arr), np.array(type_arr)


rtg = RenderedTextGenerator(batch_size=1, fontsize_range=(5, 30), fonts_folder='fonts/', img_shape=(128, 128), fonttype='bold')
imgs, txts = rtg.render_text('img.png')
print(txts[-1])
