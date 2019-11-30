from flask import Flask, request, jsonify
from http import HTTPStatus
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home () :
    body = request.get_json()
    return jsonify(status="done", content=body), HTTPStatus.OK

@app.errorhandler(404)
def error (e) :
    return jsonify(error=HTTPStatus.BAD_REQUEST),HTTPStatus.BAD_REQUEST

if __name__ == "__main__" :
    debug = bool(os.getenv('PRIVATE_DEBUG', ''))
    app.run(host='0.0.0.0', port=8000, debug=debug)