import trees as tr
import math
pi = math.pi

### Utility Functions to help plot the graph ###

def num_repeats(first, second, data):
    '''Returns the number of times an edge connecting the same 2 nodes 'first' and 'second' appears in 'data'.
       Returns 1 if the edge only appears once.'''
    num = 0
    for edge in data:
        if (first == edge[0] and second == edge[1]) or (second == edge[0] and first == edge[1]):
            num += 1
    return num

def quick_sort(lst):
    '''Sorts a list of lists 'lst' by the first element in each sublist.'''
    if not lst:
        return lst
    else:
        pivot = lst[0][0]
        a = quick_sort([x for x in lst[1:] if x[0]<pivot])
        b = quick_sort([x for x in lst[1:] if x[0]>=pivot])
        return a + [lst[0]] + b

def find_theta(x0, x1, y0, y1):
    '''Finds and returns the value of the angle, in radians, of the line going from (x0, y0) to (x1, y1).'''
    dx, dy = x1 - x0, y1 - y0
    if dx == 0:
        if dy > 0:
            theta = pi/2
        else:
            theta = -1 * pi/2
    elif dy == 0:
        if dx > 0:
            theta = 0
        else:
            theta = pi
    else:
        theta = math.atan(dy / dx)
        if dx < 0:
            theta = theta - pi

    return theta

def find_dist(x0, x1, y0, y1):
    '''Returns the distance between the points located at (x0, y0) and (x1, y1).'''
    dx, dy = x1 - x0, y1 - y0
    dx, dy = dx * dx, dy * dy
    return math.sqrt(dx + dy)
