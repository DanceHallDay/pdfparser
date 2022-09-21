from abc import ABC
from typing import Tuple
import numpy as np


class IVisualAugmenter(ABC):
    def augment(
        self, img: np.array, starts_x: np.array, ends_x: np.array
    ) -> Tuple[np.array, np.array, np.array]:
        """
        Applies augmentation technique to @img and returns an augmented image
        """
        pass
