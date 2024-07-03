import os
import json

def read_config(path):
    with open(path, 'r') as f:
        dat = json.load(f)
    img_dir = dat['img_dir']
    gt_json = dat['gt_json']
    return img_dir, gt_json

def test():
    img_dir, gt_json = read_config('./config.json')
    assert img_dir == '../dataset/images/'
    print('passed')

if __name__ == '__main__':
    test()
