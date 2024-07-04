import os
import json

def read_config(path='./config.json'):
    with open(path, 'r') as f:
        dat = json.load(f)
    img_dir = dat['img_dir']
    # gt_json = dat['gt_json']
    # return img_dir, gt_json
    return img_dir

def test():
    img_dir = read_config()
    assert img_dir == '../dataset/images/'
    print('passed')

if __name__ == '__main__':
    test()
