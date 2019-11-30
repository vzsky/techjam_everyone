import math
def distance (p1, p2, m) :
    if (m == "euclidean") : 
        return math.sqrt((p1['x'] - p2['x'])*(p1['x'] - p2['x']) + (p1['y'] - p2['y'])*(p1['y'] - p2['y']))
    if (m == "manhattan") : 
        return abs(p1['x'] - p2['x']) + abs(p1['y'] - p2['y'])

def brute(ax):
    mi = dist(ax[0], ax[1])
    p1 = ax[0]
    p2 = ax[1]
    ln_ax = len(ax)
    if ln_ax == 2:
        return p1, p2, mi
    for i in range(ln_ax-1):
        for j in range(i + 1, ln_ax):
            if i != 0 and j != 1:
                d = dist(ax[i], ax[j])
                if d < mi:  # Update min_dist and points
                    mi = d
                    p1, p2 = ax[i], ax[j]
    return p1, p2, mi

def closest_pair(ax, ay):
    ln_ax = int(len(ax)) 
    if ln_ax <= 3:
        return brute(ax)  # A call to bruteforce comparison
    mid = ln_ax // 2 
    Qx = ax[:mid] 
    Rx = ax[mid:]
    midpoint = ax[mid][0]  
    Qy = list()
    Ry = list()
    for x in ay:  # split ay into 2 arrays using midpoint
        if x[0] <= midpoint:
           Qy.append(x)
        else:
           Ry.append(x)
    # Call recursively both arrays after split
    (p1, q1, mi1) = closest_pair(Qx, Qy)
    (p2, q2, mi2) = closest_pair(Rx, Ry)
    # Determine smaller distance between points of 2 arrays
    if mi1 <= mi2:
        d = mi1
        mn = (p1, q1)
    else:
        d = mi2
        mn = (p2, q2)
    # Call function to account for points on the boundary
    (p3, q3, mi3) = closest_split_pair(ax, ay, d, mn)
    # Determine smallest distance for the array
    if d <= mi3:
        return mn[0], mn[1], d
    else:
        return p3, q3, mi3

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def closest_split_pair(p_x, p_y, delta, best_pair):
    ln_x = int(len(p_x))  # store length - quicker
    mx_x = p_x[ln_x // 2][0]  # select midpoint on x-sorted array
    # Create a subarray of points not further than delta from
    # midpoint on x-sorted array
    s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
    best = delta  # assign best value to delta
    ln_y = len(s_y)  # store length of subarray for quickness
    for i in range(ln_y - 1):
        for j in range(i+1, min(i + 7, ln_y)):
            p, q = s_y[i], s_y[j]
            dst = dist(p, q)
            if dst < best:
                best_pair = p, q
                best = dst
    return best_pair[0], best_pair[1], best

def legacy (r) :

    if 'north' in r and 'south' in r :
        raise ("dup")
    if 'east' in r and 'west' in r :
        raise ("dup")

    if 'north' in r :
        r['y'] = r['north']
    if 'south' in r :
        r['y'] = -r['south']
    if 'west' in r :
        r['x'] = -r['west']
    if 'east' in r :
        r['x'] = r['east']

    r.pop('north', None)
    r.pop('south', None)
    r.pop('east', None)
    r.pop('west', None)

    return r