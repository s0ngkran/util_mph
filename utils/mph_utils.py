import json
from dataclasses import dataclass, field
from typing import List
from swap_hand import is_pointing_hand
from tfs import pred, mph_to_tfs
from read_config import read_config
from read_data import read_data
import os
try:
    import cv2
except:
    pass


@dataclass
class MPHResult:
    gt: int 
    # hand_side: str # is_img_fliped 
    gt_keypoints: List 

    mph_keypoints: List 
    pred_tfs: str
    img_path: str
    key: str
    n_hand: int
    pointing_hand: List
    palm_hand: List
    pred_tfs_palm_kps: List
    pred_tfs_pointing_kps: List
    gt_tfs_keypoints: List
    can_pred: bool = False
    is_correct: bool = False

    def read_img(self):
        path = self.img_path
        img = cv2.imread(path)
        assert img is not None, 'img_path = %s'%path
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def __init__(self, dat, mph_keypoints, has_gt_keypoints = True):
        self.img_path = dat.img_path
        self.gt = dat.gt
        # self.hand_side = dat['hand_side']
        # assert self.hand_side in ['L', 'R']
        palm_ind_list = [0,1,3,4,5,8,9,12,13,16,17] # 20 is pinky
        if has_gt_keypoints:
            self.gt_keypoints = [(float(x), float(y)) for x,y,_ in dat['keypoint']]
            self.gt_tfs_keypoints = [self.gt_keypoints[i] for i in palm_ind_list]
        else:
            self.gt_keypoints = []
            self.gt_tfs_keypoints = []
        self.mph_keypoints = mph_keypoints
        self.n_hand = self.get_n_hand(mph_keypoints)
        r = self.do_pred(self.n_hand, mph_keypoints)
        if type(r) == str:
            r = [], [], r, [], None
        self.pointing_hand, self.palm_hand, self.pred_tfs, self.pred_tfs_palm_kps, self.pred_tfs_pointing_kps = r
        self.key = dat.img_name
        if self.n_hand == 2:
            self.can_pred = True
            self.is_correct = self.pred_tfs == self.gt

    def get_n_hand(self, keypoints):
        n = len(keypoints)
        assert n in [0, 21, 42]
        return n // 21

    def do_pred(self, n_hand, keypoints):
        if n_hand in [0, 1]:
            return 'False; hand!=2'

        # define pointing hand and palm hand
        hand1 = keypoints[:21]
        hand2 = keypoints[21:]
        assert len(hand1) == len(hand2) == 21
        
        # swap_hand_method
        # is_hand1_pointing, is_hand2_pointing = self.rule_based_original(hand1, hand2)
        is_hand1_pointing, is_hand2_pointing = self.rule_based_on_hand1(hand1, hand2)
        # is_hand1_pointing, is_hand2_pointing = self.rule_based_on_hand2(hand1, hand2)
        if is_hand1_pointing == is_hand2_pointing == True:
            return 'False; two pointing_hand'
        elif is_hand1_pointing == is_hand2_pointing == False:
            return 'False; two palm_hand'
        # pred tfs
        hands = []
        if is_hand1_pointing:
            hands = hand1 + hand2
            pointing_hand = hand1
            palm_hand = hand2
        elif is_hand2_pointing:
            hands = hand2 + hand1
            pointing_hand = hand2
            palm_hand = hand1

        kp = mph_to_gt(pointing_hand, palm_hand) # first hand == palm
        pred_result = pred(kp)
        tfs_palm_kps, _, tfs_pointing_kps = mph_to_tfs(kp, is_return_pointing_list=True)
        assert type(pred_result) == int
        return pointing_hand, palm_hand, pred_result, tfs_palm_kps, tfs_pointing_kps

    def rule_based_original(self, hand1, hand2):
        is_hand1_pointing = is_pointing_hand(hand1)
        is_hand2_pointing = is_pointing_hand(hand2)
        return is_hand1_pointing, is_hand2_pointing
    def rule_based_on_hand1(self, hand1, hand2):
        r = is_pointing_hand(hand1)
        if r:
            is_hand1_pointing = True
            is_hand2_pointing = False
        else:
            is_hand1_pointing = False
            is_hand2_pointing = True
        return is_hand1_pointing, is_hand2_pointing
    def rule_based_on_hand2(self, hand1, hand2):
        r = is_pointing_hand(hand2)
        if r:
            is_hand2_pointing = True
            is_hand1_pointing = False
        else:
            is_hand2_pointing = False
            is_hand1_pointing = True
        return is_hand1_pointing, is_hand2_pointing

    def __str__(self):
        return f'<MPH-{self.key}|gt_{self.gt}|pred_tfs{self.pred_tfs}>'

def mph_to_gt(pointing_hand, palm_hand):
    mph_keypoints = palm_hand + pointing_hand
    p0_p9 = 'middle_point'
    map = [
        0,2,3,4, 
        # p0_p9, # middle_point 
        5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
        26,27,28,29
    ]
    assert len(map) == 24

    keypoints = []
    for index in map:
        key = mph_keypoints[index]
        keypoints.append(key)
        if index == 4:
            wrist = mph_keypoints[0]
            middle_finger_mcp = mph_keypoints[9]
            x = (wrist[0] + middle_finger_mcp[0])/2
            y = (wrist[1] + middle_finger_mcp[1])/2
            middle_point = [x, y]
            keypoints.append(middle_point)
            assert len(keypoints) == 5, f'len keypoints = {len(keypoints)}'
    assert len(keypoints) == 25, f'len keypoints = {len(keypoints)}'
    return keypoints

def mph_pack():
    img_dir = read_config('./config.json')
    data = read_data()
    mph_keypoints = load_mph_result(json_path='mph_keypoints.json')
    pack = []
    for dat in data:
        key = dat.img_name
        # print('key', key)
        kps = mph_keypoints[key]
        dat = MPHResult(dat, kps, has_gt_keypoints=False)
        pack.append(dat)
    return pack

def load_mph_result(json_path='mph_result.json'):
    with open(json_path, 'r') as f:
        map = json.loads(f.read())
    # print(map)
    # example data
    # {
    #     "WIN_20210329_13_59_40_Pro.jpg": [[122, 224], ...]
    # }
    return map

