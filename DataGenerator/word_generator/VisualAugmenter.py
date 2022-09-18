from .IVisualAugmenter import IVisualAugmenter
from typing import List
import numpy as np
import cv2
import imutils



class VisualAugmenterRotation(IVisualAugmenter):
    def __init__(
        self, 
        lower: float, 
        upper: float
        ):
        """Generate random angle and rotate image by this angel.
        lower: float
            lower angle bound
        upper: float
            upper angle bound
            
        """
        self.lower = lower
        self.upper = upper

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        angle = np.random.randint(self.lower, self.upper)
        img = cv2.bitwise_not(img)
        img = imutils.rotate_bound(img, angle)
        img = cv2.bitwise_not(img)
        return img


class VisualAugmenterGaussianNoise(IVisualAugmenter):
    def __init__(
            self, 
            mean: float, 
            std: float
        ):
        """ Add gaussian noise to an image
        mean: float
            Mean of the distribution.
        std: float
            Standard deviation of the distribution. Must be non-negative.
        """
        self.mean = mean
        self.std = std

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        gaussian = np.random.normal(self.mean, self.std, img.shape).astype(np.uint8)
        img = img + gaussian
        return img


class VisualAugmenterStretching(IVisualAugmenter):
    def __init__(
            self, 
            dx: List[float], 
            dy: List[float]
        ):
        """Applies ыtretching along x and y axes.
        dx: List[float, float]
            Scale range along x axe. lower bound must be > 0.
        dy: List[float, float]
            Scale range along y axe. lower bound mest be > 0.
        Example: dx = [0.5, 1.4]
        """
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
    def __init__(
            self, 
            iteration: int, 
            kernel_size_range: List[int]
        ):
        """Erodes an image by using a specific structuring element.
        iterations: int
            number of times erosion is applied.
        kernel_range: List[int, int]
            Range for kernel size.
        """
        self.iteration = iteration
        self.kernel_size_range = kernel_size_range

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        w = np.random.randint(*self.kernel_size_range)
        h = np.random.randint(*self.kernel_size_range)
        kernel = np.random.choice([0, 1], size=(w, h)).astype(np.uint8)
        img = cv2.erode(img, kernel, iterations=self.iteration)
        return img


class VisualAugmenterDilation(IVisualAugmenter):
    def __init__(
        self, 
        iteration: int, 
        kernel_range: List[int]
        ):
        """Dilates an image by using a specific structuring element.
        iterations: int
            number of times dilation is applied.
        kernel_range: List[int, int]
            Range for kernel size.
        """
        self.iteration = iteration
        self.kernel_range = kernel_range

    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        w = np.random.randint(*self.kernel_range)
        h = np.random.randint(*self.kernel_range)
        kernel = np.random.choice([0, 1], size=(w, h)).astype(np.uint8)
        img = cv2.dilate(img, kernel, iterations=self.iteration)
        return img

