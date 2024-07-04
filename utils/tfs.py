try:
    import matplotlib.pyplot as plt
except:
    pass
from find_nearest import find_nearest_point_index

# palm_ind_list = [0,1,3,4,5,8,9,12,13,16,17,20] # 20 is pinky
palm_ind_list = [0,1,3,4,5,8,9,12,13,16,17] # 20 is pinky
pointing_ind = 24
def mph_to_tfs(mph_keys, is_return_pointing_list=False):
    assert len(mph_keys) == 25
    palm = []
    pointing = None
    pointing_list = []
    for i, k in enumerate(mph_keys):
        if i in palm_ind_list:
            palm.append(k)
        if i == pointing_ind:
            pointing = k
        if i >= 22:
            pointing_list.append(k)
    if is_return_pointing_list:
        return palm, pointing, pointing_list
    return palm, pointing

def pred(mph_keys):
    palm, pointing = mph_to_tfs(mph_keys)
    nearest_index = find_nearest_point_index(pointing, palm)
    return nearest_index 

def plot_tfs(mph_keys, nearest_index=None):
    assert len(mph_keys) == 25
    for i, k in enumerate(palm_ind_list):
        p = mph_keys[k]
        x, y = p
        c = 'go'
        # if i == 11: c = 'yo'

        if nearest_index != None and i == nearest_index: c = 'bo'
        plt.plot(x, y, c)
        plt.text(x, y+2, str(i))
    pointing = mph_keys[pointing_ind]
    x, y = pointing
    plt.plot(x, y, '>b')


def test():
    pass

if __name__ == '__main__':
    test()
