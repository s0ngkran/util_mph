import sys
import scipy 
sys.path.append('./utils')
import numpy as np
from collections import Counter
from mph_pack import MPHPack
try:
    import matplotlib.pyplot as plt
except:
    pass
    
def plot(plt, hand, color='r'):
    assert len(hand) == 11 
    line = [[0,3], [3,6], [0,1], [1,2], [4,6], [6,8], [8,10], [4,5], [6,7], [8,9]]
    for k in hand:
        plt.plot(k[0], k[1], color + 'x')
    for i, j in line:
        a, b = hand[i], hand[j]
        plt.plot([a[0], b[0]], [a[1], b[1]], color + '-')
def plot_pointing(plt, hand, color='r'):
    line =[ [0,1], [1,2], [2,3]]
    for x, y in hand[3:]:
        plt.plot(x, y, color + 'x')
    for i, j in line:
        a, b = hand[i], hand[j]
        plt.plot([a[0], b[0]], [a[1], b[1]], color + '-')
def zoom(x):
    pts = x.mph_palm_keypoints + x.mph_pointing_keypoints
    x = [p[0] for p in pts]
    y = [p[1] for p in pts]
    xmin = min(x)
    ymin = min(y)
    xmax = max(x)
    ymax = max(y)
    xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)
    offset = 10
    w, h = xmax - xmin, ymax -ymin
    # making square
    c = (xmax + xmin)/2, (ymax + ymin)/2
    wid = w if w > h else h
    xmin, xmax, ymin, ymax = c[0]-w, c[0]+w, c[1]-w, c[1]+w
    return xmin -offset, xmax+offset, ymax+offset, ymin-offset
def plot_gt_pred(plt,x):
    gt = x.gt
    pred = x.pred_tfs
    tip = x.mph_pointing_keypoints[-1]
    # plot gt and pred point
    target_p = x.mph_palm_keypoints[gt]
    plt.plot(target_p[0], target_p[1], 'lime', marker='o')
    # dist = np.linalg.norm(np.array(tip) - np.array(target_p))
    # plt.text(target_p[0], target_p[1], f'{dist:.0f}')

    target_p = x.mph_palm_keypoints[pred]
    plt.plot(target_p[0], target_p[1], 'red', marker='o')
    # dist = np.linalg.norm(np.array(tip) - np.array(target_p))
    # plt.text(target_p[0], target_p[1], f'{dist:.0f}')

def get_dist(p1, p2):
    p1, p2 = np.array(p1), np.array(p2)
    dist = np.linalg.norm(p2 - p1)
    return dist

def show(plt, x):
    img = x.read_img()
    plt.imshow(img)
    gtk = x.gt_palm_keypoints
    mpk = x.mph_palm_keypoints
    pmpk = x.mph_pointing_keypoints
    gt = x.gt
    pred = x.pred_tfs
    # plot(gtk, 'g')
    plot(plt,mpk, 'b')
    plot_pointing(plt,pmpk)
    plot_gt_pred(plt,x)


    plt.axis(zoom(x))
    title = f'gt{gt} p{pred}'
    return title
    # plt.gca().invert_yaxis()


def plot_two_hands_not_correct(o):
    print(f'{o.acc=:.2f}%')
    print(f'{o.n=} {o.n_pred_zero_hand=} {o.n_pred_one_hand=} {o.n_pred_two_hands=}')

    two = o.two
    two_n = o.two_hands_not_correct
    print(f'two hands correct = {(o.n_correct/o.n_pred_two_hands)*100}%')
    print(f'two hand not correct = {len(two_n)/o.n_pred_two_hands*100}%')

    n = len(two_n)
    col = 5
    fig, axs = plt.subplots(n//col, col, figsize=(8,4) )
    axs = axs.flatten()
    for i in range(len(two_n)):
        x = two_n[i]
        title = show(axs[i], x)
        axs[i].axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()

def check_keypoint(o):
    # for i, (a, b) in enumerate(x.gt_keypoints):
    #     if i not in [7, 12]:continue
    #     plt.plot(a, b, 'mo')
    #     plt.text(a+10, b, str(i))
    # img = x.read_img()
    # plt.imshow(img)
    # plt.show()
    pass

def shapiro_wilk(data):
    res = scipy.stats.shapiro(data)
    is_normal =  res.pvalue > 0.05 
    return res.pvalue, is_normal

def mannwhitneyu(data1, data2):
    # mann is for non-normal
    p1, is_normal1 = shapiro_wilk(data1)
    p2, is_normal2 = shapiro_wilk(data2)
    assert is_normal1 == False
    assert is_normal2 == False

    res = scipy.stats.mannwhitneyu(data1, data2)
    is_difference = res.pvalue < 0.05
    return res.pvalue, is_difference

def stat_of_two_hands(corr, fail):
    p, is_normal = shapiro_wilk(corr)
    print(f'correct => p={p} is_normal={is_normal}')
    p, is_normal = shapiro_wilk(fail)
    print(f'fail => p={p:.4f} is_normal={is_normal}')

    p, is_difference = mannwhitneyu(corr, fail)
    print(f'corr and fail is_difference={is_difference} with p-value={p:.4f}')


def plot_two_hands_box(o):
    two = o.two
    x = two[0]

    dist = x.pointing_finger_diff
    is_correct = x.is_correct

    data = {
        'Correct': [d.pointing_finger_diff for d in o.two if d.is_correct],
        'Fail': [d.pointing_finger_diff for d in o.two if not d.is_correct]
    }
    names = data.keys()
    data_group = list(data.values())
    plt.boxplot(data_group, labels=names)
    # plt.violinplot(data)
    plt.ylabel('Index finger tip error (% palm size)')

    corr = data_group[0]
    fail = data_group[1]

    stat_of_two_hands(corr, fail)

    plt.show()

def main(o):
    # plot_two_hands_not_correct(o)
    plot_two_hands_box(o)


if __name__ == '__main__':
    _, mph_path, gt_path = sys.argv
    o = MPHPack(mph_path, gt_path)
    main(o)
