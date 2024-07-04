import math

def find_nearest_point_index(point, points):
    if not points:
        return None

    nearest_index = 0
    nearest_distance = math.dist(point, points[0])  # Calculate distance to the first point

    for i in range(1, len(points)):
        distance = math.dist(point, points[i])
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_index = i

    return nearest_index

def test():
    reference_point = (0, 0)
    list_of_points = [(1, 1), (2, 2), (3, 3), (-1, -1)]

    nearest_index = find_nearest_point_index(reference_point, list_of_points)
    assert nearest_index == 0 

    reference_point = (2, 2)
    list_of_points = [(1, 1), (2, 2), (3, 3), (-1, -1)]

    nearest_index = find_nearest_point_index(reference_point, list_of_points)
    assert nearest_index == 1 
    print('all tests passed')

if __name__ == '__main__':
    test()
