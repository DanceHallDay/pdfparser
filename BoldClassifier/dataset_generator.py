#----------------------------------------------------------------------
import sys
sys.path.append('/home/ivan/pdfparser-3/DataGenerator/word_generator/')
sys.path.append('/home/ivan/pdfparser-3/DataGenerator/text_generator/')
sys.path.append('/home/ivan/pdfparser-3/DataGenerator/word_storage/')
sys.path.append('/home/ivan/pdfparser-3/DataGenerator/fonts/')
sys.path.append('/home/ivan/pdfparser-3/DataGenerator')
sys.path.append('/home/ivan/pdfparser-3')
#----------------------------------------------------------------------
import cv2
import numpy as np
from typing import List, Dict, Union, Tuple
import torch
import random
from torch.utils.data import Dataset
from IFont import IFont
from IVisualAugmenter import IVisualAugmenter
from IWordGenerator import IWordGenerator
from IWordRenderer import IWordRenderer


def feature_extractraction(img : np.array) -> np.array:
    #img to binary
    grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    (thresh, img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    img = (img - img.min()) / (img.max() - img.min())
    
    num_points = np.sum(img == 0)
    
    kernel = np.ones((3,3),np.uint8)
    kernel2 = np.ones((3,1),np.uint8)
    kernel3 = np.ones((1,3),np.uint8)
    kernel4 = np.ones((1,1),np.uint8)
    
    features = []
    
    features.append(np.sum(cv2.dilate(img,kernel4,iterations = 1) == 0) / num_points)    
    features.append(np.sum(cv2.dilate(img,kernel,iterations = 1) == 0) / num_points)    
    features.append(np.sum(cv2.dilate(img,kernel2,iterations = 1) == 0) / num_points) 
    features.append(np.sum(cv2.dilate(img,kernel2,iterations = 2) == 0) / num_points) 
    features.append(np.sum(cv2.dilate(img,kernel2,iterations = 3) == 0) / num_points)
    features.append(np.sum(cv2.dilate(img,kernel3,iterations = 1) == 0) / num_points) 
    features.append(np.sum(cv2.dilate(img,kernel3,iterations = 2) == 0) / num_points) 
    features.append(np.sum(cv2.dilate(img,kernel3,iterations = 3) == 0) / num_points) 
    
    return np.array(features)

def add_margin(img : np.array) -> np.array:
    if (img.shape[0] > 224 or img.shape[1] > 224):
        return cv2.resize(img, (224, 224))
    
    img = img[:, :, :3]
    old_image_height, old_image_width, channels = img.shape
    max_scale_coef = max(224 // max(old_image_width, old_image_height), 1)
    img = cv2.resize(img, (max_scale_coef*old_image_width, max_scale_coef*old_image_height))
    old_image_height, old_image_width, channels = img.shape

    # create new image of desired size and color (blue) for padding
    new_image_width = 224
    new_image_height = 224
    color = (255,255,255)
    result = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)

    # compute center offset
    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2

    # copy img image into center of result image
    result[y_center:y_center+old_image_height, 
           x_center:x_center+old_image_width] = img
    
    return result

class SequenceGenerator:
    def __init__(
        self,
        fonts: Dict[str, Union[List[IFont], np.array]],
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
        
    def generate_sequence(
        self, sequence_len: int
    ) -> List[Union[IWordRenderer.word_render, int]]:
        sequences = []
        font = random.choice(list(self.fonts.values()))
        font_size = np.random.choice(self.font_sizes[0], p=self.font_sizes[1])

        for _ in range(sequence_len):
            random_font = np.random.choice(font[0], p=font[1])
            #print(random_font.get_font_name())
            sequences.append(
                [
                    *self.word_renderer.word_render(
                            self.word_generator.word_generate(case=np.random.randint(1, 4)),
                            random_font,
                            font_size,
                            self.augmenters,
                        ),
                    int("bold" in random_font.get_font_name().lower())
                ]
            )
        return sequences

    
class DatasetGenerator(Dataset):
    def __init__(self, text_generator, transform=None, num_words: int = 32, mode: str = "image"):
        super(DatasetGenerator, self).__init__()
        self.text_generator = text_generator
        self.transform = transform
        self.num_words = num_words
        self.mode = mode
        
    def __len__(self):
        return 64
    
    def __getitem__(self, idx):
        imgs, labels = [], []
        gen_data = self.text_generator.generate_sequence(self.num_words)
        
        if self.transform is not None:
            for img, _, _, _, label in gen_data:
                if self.mode == 'image':
                    img = cv2.resize(img, (224, 224))
                elif self.mode == 'padding':
                    img = add_margin(img)

                imgs.append(self.transform(image = img[:, :,:3])['image'].float())
                labels.append(label)

        return  torch.stack(imgs), torch.tensor(labels) 