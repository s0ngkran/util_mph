from dataclasses import dataclass
from typing import List
import os

gt_list = [i for i in range(11)]
@dataclass
class MPHInput:
    folder: str
    img_name: str
    gt: int
    gt_keypoints: str = 'List'
    gt_palm_keypoints: str = 'List'
    img_path: str = ''

    def __post_init__(self):
        assert self.gt in gt_list
        assert '/' not in self.img_name 
        self.img_path = os.path.join(self.folder, self.img_name)
