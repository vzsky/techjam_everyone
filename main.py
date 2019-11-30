from flask import Flask, request, jsonify
from http import HTTPStatus
from calc import distance, closest_pair, legacy
import os
import re

app = Flask(__name__)

robot_positions = {}
allrobot = []
inf = float('Inf')

@app.route('/distance', methods=['POST'])
def dis () :
    r = request.get_json()
    if (type(r) is not dict) :
        return '', 400
    if (not 'first_pos' in r or not 'second_pos' in r) :
        return '', 400
    if type(r['first_pos']) is str and not re.match(r"^robot#([1-9][0-9]*)$", r['first_pos']): 
        return '', 400
    if type(r['second_pos']) is str and not re.match(r"^robot#([1-9][0-9]*)$", r['second_pos']):
        return '', 400
    
    # robot
    if type(r['first_pos']) is str and re.match(r"^robot#([1-9][0-9]*)$", r['first_pos']):
        robot_id = int(r['first_pos'].split('#')[1])
        # print(robot_id)
        if (not robot_id in robot_positions) :
            return '', 424
        r['first_pos'] = robot_positions[robot_id]
    if type(r['second_pos']) is str and re.match(r"^robot#([1-9][0-9]*)$", r['second_pos']):
        robot_id = int(r['second_pos'].split('#')[1])
        # print(robot_id)
        if (not robot_id in robot_positions) :
            return '', 424
        r['second_pos'] = robot_positions[robot_id]

    #legacy
    try :
        r['first_pos'] = legacy(r['first_pos'])
        r['second_pos'] = legacy(r['second_pos'])
    except :
        return '', 400

    metric = "euclidean"
    if ('metric' in r) :
        metric = r['metric']
        if metric != 'euclidean' and metric != "manhattan" :
            return '', 400

    # print(r['first_pos'])
    # print(r['second_pos'])
    return jsonify(distance=distance(r['first_pos'], r['second_pos'], metric)), 200

@app.route('/robot/<robot_id>/position', methods=['GET','PUT'])
def pos (robot_id) :
    robot_id = int(robot_id)
    r = request.get_json()
    if (type(r) is not dict) :
        return '', 400
    if (request.method == 'PUT') :
        if (robot_id < 1 or robot_id > 999999 or not 'position' in r) :
            return '', 400
        try :
            r['position'] = legacy(r['position'])
        except :
            return '', 400
        r['position'] = legacy(r['position'])
        robot_positions[robot_id] = r["position"]
        if robot_id not in allrobot :
            allrobot.append(robot_id)
        return '', 204
    if (request.method == 'GET') :
        if robot_id in robot_positions :
            return jsonify(position=robot_positions[robot_id]), 200
        else :
            return '',404
    raise("error")

@app.route('/nearest', methods = ['POST'])
def near () :
    r = request.get_json()
    if (type(r) is not dict) :
        return '', 400
    if not 'ref_position' in r :
        return '', 400 
    k = 1
    if ('k' in r) :
        if (r['k'] < 1) :
            return '', 400
        k = r['k']
    minimum = []
    dist = {}
    metric = "euclidean"
    for id in robot_positions : 
        d = distance(robot_positions[id], r['ref_position'], metric)
        minimum.append(id)
        dist[id] = d
    minimum.sort(key=lambda v: dist[v])
    if len(robot_positions) == 0 :
        return jsonify(robot_ids=[]), 200
    return jsonify(robot_id=sorted(sorted(minimum[:k]), key=lambda v: dist[v])), 200

@app.route('/closestpair', methods=['GET'])
def closepair() :
    if len(allrobot) < 2 :
        return '', 424
    a = [(robot_positions[d]['x'], robot_positions[d]['y']) for d in allrobot]
    ax = sorted(a, key=lambda x : x[0])
    ay = sorted(a, key=lambda x : x[1])
    print(ax)
    print(ay)
    p1, p2, d = closest_pair(ax, ay)
    return jsonify(distance=d), 200


if __name__ == "__main__" :
    debug = bool(os.getenv('PRIVATE_DEBUG', ''))
    app.run(host='0.0.0.0', port=8000, debug=debug)