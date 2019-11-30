from flask import Flask, request, jsonify
from http import HTTPStatus
from calc import distance
import os
import re

app = Flask(__name__)

robot_positions = {'1' : {'x' : 1, 'y' : 1}}

@app.route('/distance', methods=['POST'])
def dis () :
    r = request.get_json()
    if type(r['first_pos']) is str and re.match(r"^robot#([1-9][0-9]*)$", r['first_pos']):
        robot_id = r['first_pos'].split('#')[1]
        if (not robot_id in robot_positions) :
            return '', 424
        r['first_pos'] = robot_positions[robot_id]
    if type(r['second_pos']) == 'str' and re.match(r"^robot#([1-9][0-9]*)$", r['second_pos']):
        robot_id = r['first_pos'].split('#')[1]
        if (not robot_id in robot_positions) :
            return '', 424
        r['second_pos'] = robot_positions[robot_id]


    metric = "euclidean"
    if ('metric' in r) :
        metric = r['metric']

    return jsonify(distance=distance(r['first_pos'], r['second_pos'], metric)), 200

@app.route('/robot/<robot_id>/position', methods=['GET','PUT'])
def pos (robot_id) :
    r = request.get_json()
    if (request.method == 'PUT') :
        robot_positions[robot_id] = r["position"]
        return '', 204
    if (request.method == 'GET') :
        if robot_id in robot_positions :
            return jsonify(position=robot_positions[robot_id]), 200
        else :
            return '',404

# @app.errorhandler(400)
# def error400 (e) :
#     return '',400
# @app.errorhandler(404)
# def error404 (e) :
#     return '',404

if __name__ == "__main__" :
    debug = bool(os.getenv('PRIVATE_DEBUG', ''))
    app.run(host='0.0.0.0', port=8000, debug=debug)