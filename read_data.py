import json
from utils.mph_input import MPHInput
from utils.read_config import read_config
from collections import Counter

def read_data():
    path = '../data_zip/poh_plain_vs_natural/replaced/replaced_bg.poh_black_testing.json'
    with open(path, 'r') as f:
        data = json.load(f)
    folder = read_config()


    mph_input_list = []
    for v in data:
        img_name = v['img_path'].split('/')[-1]
        gt = ord(v['gt']) - 65
        gt = custom_gt_for_vr_poh_1k(gt)
        obj = MPHInput(folder, img_name,  gt)
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

