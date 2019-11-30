import math
def distance (p1, p2, m) :
    if (m == "euclidean") : 
        return math.sqrt((p1['x'] - p2['x'])*(p1['x'] - p2['x']) + (p1['y'] - p2['y'])*(p1['y'] - p2['y']))
    if (m == "manhattan") : 
        return abs(p1['x'] - p2['x']) + abs(p1['y'] - p2['y'])