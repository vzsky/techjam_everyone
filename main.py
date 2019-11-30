from flask import Flask, request, jsonify
from http import HTTPStatus
from calc import distance
import os

app = Flask(__name__)

@app.route('/distance', methods=['POST'])
def home () :
    r = request.get_json()
    return jsonify(distance=distance(r['first_pos'], r['second_pos'])), HTTPStatus.OK

@app.errorhandler(404)
def error (e) :
    return jsonify(),HTTPStatus.BAD_REQUEST

if __name__ == "__main__" :
    debug = bool(os.getenv('PRIVATE_DEBUG', ''))
    app.run(host='0.0.0.0', port=8000, debug=debug)