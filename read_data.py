import json
from utils.mph_input import MPHInput
from utils.read_config import read_config

def read_data():
    path = '../data_zip/poh_plain_vs_natural/processed/poh_black_testing.json'
    with open(path, 'r') as f:
        data = json.load(f)
    folder = read_config()


    mph_input_list = []
    for v in data:
        img_name = v['img_path'].split('/')[-1]
        gt = ord(v['gt']) - 65
        gt = custom_gt_for_vr_poh_1k(gt)
        if 'keypoint' in v:
            kps = v['keypoint']
            img_size = 720
            gt_keypoints = [(float(k[0])*img_size, float(k[1])*img_size) for k in kps]
            gt_palm_keypoints = [gt_keypoints[i] for i in [7,8,9,18,11,10,12,13,15,14,16]]
        else: 
            gt_keypoints = []
            gt_palm_keypoints = []
        obj = MPHInput(folder, img_name,  gt, gt_keypoints, gt_palm_keypoints)
        mph_input_list.append(obj)
    # return list of MPHInput
    return mph_input_list

def custom_gt_for_vr_poh_1k(gt):
    '''
    convert to 

    5 7 9 [ ]
    | | | |
    | | | |
    | | | |
    4 6 8 10
2

  1    3

       0


    FROM 

    3 5 7 [ ]
    | | | |
    | | | |
    | | | |
    4 6 8 9
2

  1    10

       0
    '''
    #              0 1 2 3 4 5 6 7 8 9 10
    convert_key = [0,1,2,5,4,7,6,9,8,10,3]
    return convert_key[gt]

def test():
    data = read_data()
    print(data[0])
    # expect something like
    # MPHInput(img_name='266.jpg', gt=6)

if __name__ == '__main__':
    test()

