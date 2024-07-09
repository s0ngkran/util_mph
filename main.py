import sys
sys.path.append('./utils')
from mph_utils import mph_pack
from collections import Counter
try:
    import matplotlib.pyplot as plt
except:
    pass

def disp(w):
    out = f'''
    {w[5]}  {w[7]}  {w[9]}   [ ]
     |        |       |       |
     |        |       |       |
     |        |       |       |
    {w[4]}--{w[6]}--{w[8]}--{w[10]}
              |
{w[2]}        |
   \        {w[3]}
    {w[1]}    |
       \      |
        \_{w[0]}
    '''
    return out

def plot(dat, text='', raw_pred=False):
    img = dat.read_img()
    plt.imshow(img)
    title = f'{text} gt={dat.gt} res={dat.pred_tfs}'
    plt.title(title)
    gt_kp = dat.gt_tfs_keypoints
    for i, (x, y) in enumerate(gt_kp):
        plt.plot(x, y, 'yo')
        plt.text(x, y, str(i))

    kp = dat.pred_tfs_palm_kps
    # kp = dat.pointing_hand
    # kp = dat.palm_hand
    for i, (x,y) in enumerate(kp):
        plt.plot(x, y, 'b.')
    pointing_kps = dat.pred_tfs_pointing_kps
    x = []
    y = []
    try:
        for xi, yi in pointing_kps:
            x.append(xi)
            y.append(yi)
        plt.plot(x, y, '-b')
    except:
        pass
    if raw_pred:
        kp = dat.mph_keypoints
        for i, (x, y) in enumerate(kp):
            plt.plot(x, y, 'yo')
    plt.show()

def main():
    argv = sys.argv
    method = argv[1]
    mph = mph_pack(method)

    correct = 0
    can_pred = 0
    all = len(mph)
    print('method =',method)
    print('all mph', all)
    why_fail = []
    correct_list = []
    all_list = []
    force_correct_list = []
    # gt = 8

    for dat in mph:
        why_fail.append(dat.pred_tfs)
        all_list.append(dat.gt)
        if dat.can_pred == False: 
            # plot(dat, 'cannot pred', True)
            continue
        # if dat.gt == gt:
        #     plot(dat)
        #     gt+=1
        #     continue


        # plot(dat, 'can pred')
        # continue

        can_pred += 1
        if dat.is_correct:
            correct += 1
            correct_list.append(dat.pred_tfs)
        if dat.is_force_h1_correct:
            force_correct_list.append('fh1')
        if dat.is_force_h2_correct:
            force_correct_list.append('fh2')

    print(f'{can_pred=} {can_pred/all*100:.2f}%')
    print(f'{correct=} {correct/all*100:.2f}%')

    ff = Counter(force_correct_list)
    print(f'force method {len(force_correct_list)=} {len(force_correct_list)/all*100:.2f}%')
    print(f'{ff}')
    print('---')
    w = Counter(why_fail)
    a = Counter(all_list)
    c = Counter(correct_list)

    for i in range(11):
        all = a[i]
        true = c[i]
        p = true/all*100
        w[i] = f'{p:.2f}%'
    print('true/all')
    print(disp(w))

if __name__ == '__main__':
    main()
