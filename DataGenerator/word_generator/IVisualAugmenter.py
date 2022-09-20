from abc import ABC
from typing import Tuple
import numpy as np


class IVisualAugmenter(ABC):
    def augment(self, img: np.array, starts_x: np.array, ends_x: np.array) -> Tuple[np.array, np.array, np.array]:
        """
        Applies augmentation technique to @img, @starts_x and @ends_x and returns an augmented image and letters coordinates 
        """
        pass
