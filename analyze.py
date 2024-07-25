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

def check_mph_keypoint(x):
    img = x.read_img()
    plt.imshow(img)
    hands = x.mph_keypoints
    for i, (a, b) in enumerate(hands):
        if i not in [5,8]:continue
        plt.plot(a, b, 'rx', markersize=1, markeredgewidth=1)
        plt.text(a+10, b, str(b))
    # plt.title(str(len(x.gt_keypoints)))
    plt.show()
def check_keypoint(x):
    img = x.read_img()
    plt.imshow(img)
    first = [
        [0,1],
        [1,2],
        [2,3],
        [3,4],
    ]
    mid = [
        [4,5],
    ]
    last = [
        [5,6],
        [6,7],
        [7,8],
        [8,9],
        [7,18],
        [12,18],
        [10,11],
        [12,13],
        [14,15],
        [16,17],
        [16,15],
        [15,12],
        [12,11],

    ]
    hand = x.gt_keypoints
    lines = first
    for i, j in lines:
        a, b = hand[i], hand[j]
        plt.plot([a[0], b[0]], [a[1], b[1]], '-b')
    lines = mid
    for i, j in lines:
        a, b = hand[i], hand[j]
        plt.plot([a[0], b[0]], [a[1], b[1]], '-b')
    lines = last
    for i, j in lines:
        a, b = hand[i], hand[j]
        plt.plot([a[0], b[0]], [a[1], b[1]], '-g')
    # x-mark
    for i, (a, b) in enumerate(x.gt_keypoints):
        # if i not in [0,1,18,15]:continue
        plt.plot(a, b, 'rx', markersize=10, markeredgewidth=3)
        # plt.text(a+10, b, str(i))
    # plt.title(str(len(x.gt_keypoints)))
    plt.show()

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
def print_causes_fail(o):
    print(f'{o.n_pred_zero_hand/o.n*100:.2f}')
    print(f'{o.n_pred_one_hand/o.n*100:.2f}')
    print(f'{(o.n_pred_two_hands-o.n_correct)/o.n*100:.2f}')
    print(f'{o.n_correct/o.n*100:.2f}')
    pass

def plot_causes_fail():
    data = {
        'correct - two hands': 60.40,
        'fail - two hands': 6.71,
        'fail - one hand': 31.54,
        'fail - zero hand': 1.34,
    }
    labels = list(data.keys())
    values = list(data.values())

    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 14}

    plt.figure(facecolor='red')
    plt.rc('font', **font)
    colors = ['green', 'mistyrose', 'salmon', 'red']
    plt.pie(values,startangle=90,autopct='%1.1f%%', colors=colors, labels=labels)
    plt.show()

def plot_palm_ov_correct_fail(o):
    two = o.two
    ov_correct = [p.percent_palm_overlap for p in two if p.is_correct] 
    ov_fail = [p.percent_palm_overlap for p in two if not p.is_correct] 

    data = {
        'Correct': ov_correct,
        'Fail': ov_fail,
    }
    names = data.keys()
    data_group = list(data.values())
    plt.boxplot(data_group, labels=names)
    plt.ylabel('Palm overlapping (%)')

    res = mannwhitneyu(ov_correct, ov_fail)
    print(f'correct fail {res[0]:.4f}', res[1])
    plt.show()

def plot_palm_ov_index_fing(o):
    two = o.two
    for p in two:
        ov = p.percent_palm_overlap
        err = p.pointing_finger_diff
        c = p.is_correct
        color = 'xg' if c else 'xr'
        plt.plot(ov, err, color)
    plt.xlabel('Palm overlapping (%)')
    plt.ylabel('Index finger error (% palm)')
    plt.show()
def plot_hand_overlap_correct_fail(o):
    two = o.two
    ov_cor = [p.hand_overlap for p in two if p.is_correct]
    ov_fail = [p.hand_overlap for p in two if not p.is_correct]
    plt.boxplot([ov_cor, ov_fail])
    plt.show()

    res = shapiro_wilk(ov_cor)
    print(res)
    res = shapiro_wilk(ov_fail)
    print(res)

    # res = mannwhitneyu(ov_cor, ov_fail)

def plot_hand_ov_one_two(o):
    one = o.one
    two = o.two
    # one_ov = [p.hand_overlap for p in one]
    # two_ov = [p.hand_overlap for p in two]
    one_ov = [p.percent_palm_overlap for p in one]
    two_ov = [p.percent_palm_overlap for p in two]
    plt.boxplot([one_ov, two_ov])
    plt.show()
    
def plot_palm_ov_one_two(o):
    one = o.one
    two = o.two
    zero = o.zero
    # print(len(zero))
    # plt.imshow(zero[1].read_img())
    # plt.show()
    # 1/0
    # one_ov = [p.hand_overlap for p in one]
    # two_ov = [p.hand_overlap for p in two]
    one_ov = [p.percent_palm_overlap for p in one]
    two_ov = [p.percent_palm_overlap for p in two]
    zero_ov = [p.percent_palm_overlap for p in zero]
    data = {
        'Zero hand': zero_ov,
        'One hand': one_ov,
        'Two hands': two_ov,
    }
    print(len(zero), len(one), len(two))
    names = data.keys()
    data_group = list(data.values())
    plt.boxplot(data_group, labels=names)
    plt.ylabel('Palm overlapping (%)')
    plt.title('MPH-detected hands')

    res = mannwhitneyu(one_ov, two_ov)
    print(f'one two is_diff={res[1]} p={res[0]:.4e}')
    res = mannwhitneyu(zero_ov, two_ov)
    print(f'zero two is_diff={res[1]} p={res[0]:.6f}')
    plt.show()

def cir_palm(mid_point, ref_point):
    point1 = np.array(mid_point)
    point2 = np.array(ref_point)
    
    vector = point2 - point1
    radius = np.linalg.norm(vector) 
    center = mid_point
    return center, radius

def plot_cir(center, radius):
    # plot(center, color='go')
    # plot(midpoint, color='go')
    cir = plt.Circle(center, radius, edgecolor='g', facecolor='none')
    plt.gca().add_patch(cir)
def cir_pointing(p1, p2, is_flip):
    center, midpoint, radius = create_vector(p1, p2, is_flip)
    return center, radius
def create_vector(point1, point2, is_flip):
    point1 = np.array(point1)
    point2 = np.array(point2)
    
    vector = point2 - point1
    dist = np.linalg.norm(vector) * .5
    
    midpoint = point1 + 0.5 * vector
    
    scaled_vector = 0.5 * vector
    
    # rotated_vector = rotate_vector(scaled_vector, -135 )
    angle = -135 if is_flip else 135
    rotated_vector = rotate_vector(scaled_vector, angle)
    
    new_endpoint = point1 + rotated_vector
    
    return new_endpoint, midpoint, dist

def rotate_vector(vector, angle_degrees):
    angle_radians = np.deg2rad(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])
    return np.dot(rotation_matrix, vector)
def img_out(o):

        # mid = keypoints[18]
        # mid_mcp = keypoints[15]
        # c1, r1 = cir_palm(mid, mid_mcp)

        # index_tip = keypoints[0]
        # index_mcp = keypoints[1]
        # is_flip = True
        # c2, radius_unused = cir_pointing(index_tip, index_mcp, is_flip)
        # percent = get_intersect_percent(c1, c2, r1, r1)
    n = len(o.two)
    for i in range(n):
        x = o.two[i]
        print(i, n, x.percent_palm_overlap)
        plt.imshow(x.read_img())
        keypoints = x.gt_keypoints
        
        mid = keypoints[18]
        mid_mcp = keypoints[15]
        c1, r1 = cir_palm(mid, mid_mcp)
        plot_cir(c1, r1)
        index_tip = keypoints[0]
        index_mcp = keypoints[1]
        is_flip = True
        c2, radius_unused = cir_pointing(index_mcp, index_tip, is_flip)
        plot_cir(c2, r1)
        # percent = get_intersect_percent(c1, c2, r1, r1)

        for i, (a, b) in enumerate(x.gt_keypoints):
            plt.plot(a,b,'bo')
            plt.text(a,b, str(i))
        plt.title(f'ov {x.percent_palm_overlap}% h{x.n_hand} {x.key}')
        # plt.savefig('.temp/two/'+x.key)
        plt.show()
        break
    # plt.show()
    
def main(o):
    # plot_two_hands_not_correct(o)
    # plot_two_hands_box(o)
    # print_causes_fail(o)
    # plot_causes_fail()
    # plot_palm_ov_correct_fail(o)
    # plot_palm_ov_index_fing(o)
    # plot_palm_ov_one_two(o)
    # plot_hand_overlap_correct_fail(o)
    # plot_hand_ov_one_two(o)
    # img_out(o)

    # two = o.two

    # two_corr = [p for p in two if p.is_correct] 
    # # for i in range(len(two_corr)):
    # #     x = two_corr[i]
    # #     plt.title(str(i))
    # #     check_keypoint(x)
    # i = 9
    # x = two_corr[i]
    # plt.title(str(i))
    x = o.two[0]
    check_mph_keypoint(x)
    pass


if __name__ == '__main__':
    _, mph_path, gt_path = sys.argv
    o = MPHPack(mph_path, gt_path)
    main(o)
