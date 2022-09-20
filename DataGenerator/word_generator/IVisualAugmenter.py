from abc import ABC
import numpy as np


class IVisualAugmenter(ABC):
    def augment(self, img: np.array, *args, **kwrgs) -> np.array:
        """
        Applies augmentation technique to @img and returns an augmented image
        """
        pass
