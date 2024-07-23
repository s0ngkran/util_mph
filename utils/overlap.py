
from shapely.geometry import Point, Polygon
import math
import matplotlib.pyplot as plt
import numpy as np

def get_area_cir(radius):
    return math.pi * radius *radius

def plot_cir(center, radius):
    # plot(center, color='go')
    # plot(midpoint, color='go')
    cir = plt.Circle(center, radius, edgecolor='g', facecolor='none')
    plt.gca().add_patch(cir)

def get_intersect_percent(c1, c2, r1, r2):
  assert r1 == r2
  circle1 = Polygon(Point(c1[0], c1[1]).buffer(r1))
  circle2 = Polygon(Point(c2[0], c2[1]).buffer(r2))

  intersection = circle1.intersection(circle2)

  if intersection.is_empty:
    return 0

  percent = (intersection.area / circle1.area )*100

  # return intersection.area, circle1.area
  return percent

def cir_palm(mid_point, ref_point):
    point1 = np.array(mid_point)
    point2 = np.array(ref_point)
    
    vector = point2 - point1
    radius = np.linalg.norm(vector) 
    center = mid_point
    return center, radius

def rotate_vector(vector, angle_degrees):
    angle_radians = np.deg2rad(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])
    return np.dot(rotation_matrix, vector)

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

def plot(point, color='ro'):
    plt.plot(point[0], point[1], color)
    return

def cir_pointing(p1, p2, is_flip):
    center, midpoint, radius = create_vector(p1, p2, is_flip)
    return center, radius


def test():
    c1 = (1, 1)
    c2 = (1.1, 1)
    r1 = 2
    r2 = 2
    plt.plot(c1[0], c1[1], 'ro')
    plt.plot(c2[0], c2[1], 'ro')
    plot_cir(c1, r1)
    plot_cir(c2, r2)

    pr = get_intersect_percent(c1, c2, r1, r2)
    print(f"percent overlap: {pr:.2f} %")
    plt.axis('scaled')
    plt.show()


if __name__ == '__main__':
    test()

