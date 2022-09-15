from email.mime import image
from .IVisualAugmenter import IVisualAugmenter
from typing import List
import numpy as np
import cv2
from PIL import Image



class VisualAugmenterRotation(IVisualAugmenter):
    def __init__(self, rotate_range: List[int]):
        self.rotate_range = rotate_range

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        img = Image.fromarray(img)
        angle = np.random.randint(*self.rotate_range)
        img = img.rotate(angle, expand=True, fillcolor=255)
        return np.array(img).astype(np.uint8)


class VisualAugmenterGaussianNoise(IVisualAugmenter):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        gaussian = np.random.normal(self.mean, self.std, img.shape)
        noisy_image = img + gaussian
        noisy_image = noisy_image.astype(np.uint8)
        return noisy_image


class VisualAugmenterStretching(IVisualAugmenter):
    def __init__(self, dx: List[float], dy: List[float]):
        self.dx = dx
        self.dy = dy

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        rxl, rxu = int(self.dx[0] * 100), int(self.dx[1] * 100)
        ryl, ryu = int(self.dy[0] * 100), int(self.dy[1] * 100)

        width = int(img.shape[1] * np.random.randint(rxl, rxu) / 100)
        height = int(img.shape[0] * np.random.randint(ryl, ryu) / 100)
        img = cv2.resize(img, (width, height))
        return img


class VisualAugmenterStretching(IVisualAugmenter):
    def __init__(self, dx: List[float], dy: List[float]):
        self.dx = dx
        self.dy = dy

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        rxl, rxu = int(self.dx[0] * 100), int(self.dx[1] * 100)
        ryl, ryu = int(self.dy[0] * 100), int(self.dy[1] * 100)

        width = int(img.shape[1] * np.random.randint(rxl, rxu) / 100)
        height = int(img.shape[0] * np.random.randint(ryl, ryu) / 100)
        img = cv2.resize(img, (width, height))
        return img


class VisualAugmenterErosion(IVisualAugmenter):
    def __init__(self, iteration: int, kernel_range: List[int]):
        self.iteration = iteration
        self.kernel_range = kernel_range

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        w = np.random.randint(*self.kernel_range)
        h = np.random.randint(*self.kernel_range)
        kernel = np.random.choice([0, 1], size=(w, h)).astype(np.uint8)
        img = cv2.erode(img, kernel, iterations=self.iteration)
        return img


class VisualAugmenterDilation(IVisualAugmenter):
    def __init__(self, iteration: int, kernel_range: List[int]):
        self.iteration = iteration
        self.kernel_range = kernel_range

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        w = np.random.randint(*self.kernel_range)
        h = np.random.randint(*self.kernel_range)
        kernel = np.random.choice([0, 1], size=(w, h)).astype(np.uint8)
        img = cv2.dilate(img, kernel, iterations=self.iteration)
        return img

