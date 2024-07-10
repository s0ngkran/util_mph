import math
import numpy as np

def angle_between_vectors(vector1, vector2):
    dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))
    
    magnitude1 = math.sqrt(sum(v ** 2 for v in vector1))
    magnitude2 = math.sqrt(sum(v ** 2 for v in vector2))
    
    cos_angle = dot_product / (magnitude1 * magnitude2)
    
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

def mean_vectors(v1, v2, v3):
    (x1, y1), (x2, y2) = v1
    (x3, y3), (x4, y4) = v2
    (x5, y5), (x6, y6) = v3
    vector1 = np.array([x2 - x1, y2 - y1])
    vector2 = np.array([x4 - x3, y4 - y3])
    vector3 = np.array([x6 - x5, y6 - y5])
    mean_vector = (vector1 + vector2 + vector3) / 3.0
    return mean_vector

def get_vector(v1):
    (x1, y1), (x2, y2) = v1
    vector1 = np.array([x2 - x1, y2 - y1])
    return vector1

def get_angle(mph_keypoints):
    assert len(mph_keypoints) == 21
    pointing = [5,8]
    point_mid_ring_pink_ind = [[9,12], [13,16], [17,20]]
    mrp = [(mph_keypoints[p1], mph_keypoints[p2]) for p1, p2 in point_mid_ring_pink_ind]
    mrp_vector = ((0,0), mean_vectors(*mrp))
    pointing_vector = (mph_keypoints[pointing[0]], mph_keypoints[pointing[1]])
    v1 = mrp_vector
    v2 = pointing_vector

    (x1, y1), (x2, y2) = v1
    (x3, y3), (x4, y4) = v2
    
    vector1 = np.array([x2 - x1, y2 - y1])
    vector2 = np.array([x4 - x3, y4 - y3])
    return angle_between_vectors(vector1, vector2)

def get_angle_each(mph_keypoints):
    assert len(mph_keypoints) == 21

    pointing = [5,8]
    point_mid_ring_pink_ind = [[9,12], [13,16], [17,20]]
    mrp = [(mph_keypoints[p1], mph_keypoints[p2]) for p1, p2 in point_mid_ring_pink_ind]

    angles = []
    for i in range(3):
        mrp_vector = ((0,0), get_vector(mrp[i]))
        pointing_vector = (mph_keypoints[pointing[0]], mph_keypoints[pointing[1]])

        v1 = mrp_vector
        v2 = pointing_vector

        (x1, y1), (x2, y2) = v1
        (x3, y3), (x4, y4) = v2
        
        vector1 = np.array([x2 - x1, y2 - y1])
        vector2 = np.array([x4 - x3, y4 - y3])
        angle = angle_between_vectors(vector1, vector2)
        angles.append(angle)
    sum_angle = sum(angles)
    assert type(sum_angle) == float
    return sum_angle

def get_dist_pointing(mph_keypoints):
    assert len(mph_keypoints) == 21

    index_finger_tip = mph_keypoints[8]
    index_finger_tip = np.array(index_finger_tip)
    mid_ring_pink_ind = [12, 16, 20]

    dists = []
    for ind in mid_ring_pink_ind:
        p = np.array(mph_keypoints[ind])
        dist = np.linalg.norm(p - index_finger_tip)
        dists.append(dist)
    return sum(dists)

def test():
    vector1 = [1, 0]
    vector2 = [0, 1]
    angle = angle_between_vectors(vector1, vector2)
    assert angle == 90

    vector1 = [.5, .5]
    vector2 = [0, 1]
    angle = angle_between_vectors(vector1, vector2)
    # print('angle', angle)
    assert 44.9 < angle < 45.1

    print('passed')
    

if __name__ == '__main__':
    test()
