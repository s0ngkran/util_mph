import numpy as np

def is_dot_prod_less_than_zero(v1, v2):
    # print(v1)
    # print(v2)
    # exit()
    (x1, y1), (x2, y2) = v1
    (x3, y3), (x4, y4) = v2
    
    vector1 = np.array([x2 - x1, y2 - y1])
    vector2 = np.array([x4 - x3, y4 - y3])
    # print(f'{vector1=}')
    # print(f'{vector2=}')
    
    dot_product = np.dot(vector1, vector2)
    
    # If the dot product is negative, the angle is greater than 90 degrees
    return dot_product < 0


def mean_vectors(v1, v2, v3):
    (x1, y1), (x2, y2) = v1
    (x3, y3), (x4, y4) = v2
    (x5, y5), (x6, y6) = v3
    vector1 = np.array([x2 - x1, y2 - y1])
    vector2 = np.array([x4 - x3, y4 - y3])
    vector3 = np.array([x6 - x5, y6 - y5])
    mean_vector = (vector1 + vector2 + vector3) / 3.0
    return mean_vector

def is_first_hand_pointing(mph_keypoints):
    assert len(mph_keypoints) == 42
    point_mid_ring_pink_ind = [[5,8],[9,12], [13,16], [17,20]]
    pointing_vector = None
    mrp_vector = None
    mrp = []
    for i, (p1_ind, p2_ind) in enumerate(point_mid_ring_pink_ind):
        vec = mph_keypoints[p1_ind], mph_keypoints[p2_ind]
        if i == 0:
            # pointing finger
            pointing_vector = vec
        else:
            mrp.append(vec)
    assert len(mrp) == 3
    mrp_vector = mean_vectors(mrp[0], mrp[1], mrp[2])
    mrp_vector = ((0,0), mrp_vector)

    return is_dot_prod_less_than_zero(pointing_vector, mrp_vector)

def is_pointing_hand(mph_keypoints):
    # if not pointing_hand -> palm hand
    assert len(mph_keypoints) == 21
    pointing = [5,8]
    point_mid_ring_pink_ind = [[9,12], [13,16], [17,20]]
    mrp = [(mph_keypoints[p1], mph_keypoints[p2]) for p1, p2 in point_mid_ring_pink_ind]
    mrp_vector = ((0,0), mean_vectors(*mrp))
    pointing_vector = (mph_keypoints[pointing[0]], mph_keypoints[pointing[1]])
    res = is_dot_prod_less_than_zero(pointing_vector, mrp_vector)
    return res

def is_pointing_hand_paper(mph_keypoints):
    assert len(mph_keypoints) == 21
    pointing = [5,8]
    point_mid_ring_pink_ind = [[9,12], [13,16], [17,20]]
    mrp = [(mph_keypoints[p1], mph_keypoints[p2]) for p1, p2 in point_mid_ring_pink_ind]

    res = []
    for  m in mrp:
        pointing_vector = (mph_keypoints[pointing[0]], mph_keypoints[pointing[1]])
        r = is_dot_prod_less_than_zero(pointing_vector, m)
        res.append(r)
    assert len(res) == 3
    # all res == True (less than zero); pointing-hand
    res = all(res)
    assert type(res) is bool
    return res
def is_open_palm_paper(mph_keypoints):
    inds = [[5,8],[9,12], [13,16], [17,20]]
    result_y = [mph_keypoints[p8][1] < mph_keypoints[p5][1] for p5,p8 in inds  ]
    # checked
    # y 0 is top
    # y 720 is bottom

    vec42 = mph_keypoints[2], mph_keypoints[4]
    vec02 = mph_keypoints[2], mph_keypoints[0]
    res = is_dot_prod_less_than_zero(vec42, vec02)
    return all(result_y) and res

def test():
    v1 = [(0, 0), (20, 2)] 
    v2 = [(0, 0), (20, 3)]
    assert is_dot_prod_less_than_zero(v1, v2) == False

    v1 = [(0, 0), (2, 2)] 
    v2 = [(0, 0), (-2, -3)]
    assert is_dot_prod_less_than_zero(v1, v2) == True

    print('all tests passed')

if __name__ == '__main__':
    test()

