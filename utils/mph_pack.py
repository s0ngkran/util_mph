from dataclasses import dataclass
from typing import List
from mph_utils import mph_pack
@dataclass
class MPHPack:
    mph_keypoint_path: str
    gt_keypoint_path: str
    pack: List
    n: int 
    acc: float
    n_pred_two_hands: int
    n_pred_one_hand: int
    n_pred_zero_hand: int
    n_correct: int
    n_force_correct: int
    two_hands_not_correct: List
    two: List
    one: List
    zero: List

    def __init__(self, mph_path, gt_path):
        method = 'depth' # MPHZ
        self.pack = mph_pack(method, mph_path, gt_path)
        self.mph_keypoint_path = mph_path
        self.gt_keypoint_path = gt_path
        self.n = len(self.pack)
        self.two = self.get_pred_two_hand()
        self.one = self.get_pred_one_hand()
        self.zero = self.get_pred_zero_hand()
        self.n_pred_two_hands = len(self.two)
        self.n_pred_one_hand = self.get_n_pred_one_hand()
        self.n_pred_zero_hand = self.get_n_pred_zero_hand()
        self.n_correct = self.get_n_correct()
        self.acc = self.n_correct/self.n
        self.n_force_correct = self.get_n_force_correct()
        self.two_hands_not_correct = self.get_two_hands_not_correct()


    def get_n_correct(self):
        result = [1 for p in self.pack if p.is_correct]
        return len(result)
    def get_pred_zero_hand(self):
        res = [p for p in self.pack if p.n_hand == 0]
        return res 
    def get_pred_one_hand(self):
        res = [p for p in self.pack if p.n_hand == 1]
        return res 
    def get_pred_two_hand(self):
        res = [p for p in self.pack if p.n_hand == 2]
        return res 
    def get_n_pred_one_hand(self):
        res = [1 for p in self.pack if p.n_hand == 1]
        return len(res)
    def get_n_pred_zero_hand(self):
        res = [1 for p in self.pack if p.n_hand == 0]
        return len(res)
    def get_n_force_correct(self):
        res = [1 for p in self.pack if p.is_force_correct ]
        return len(res)
    def get_two_hands_not_correct(self):
        res = [p for p in self.pack if p.n_hand == 2 and p.is_correct == False]
        return res
