import os

from flask import Flask, request

from db import Base, engine
from resources.user import User

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/users', methods=['POST'])
def create_user():
    req_data = request.get_json()
    return User.create(req_data)


@app.route('/users/authenticate', methods=['POST'])
def authenticate():
    req_data = request.get_json()
    return User.authenticate(req_data)


@app.route('/users/<d_id>', methods=['PUT'])
def update_user(d_id):
    req_data = request.get_json()
    return User.update(d_id, req_data)


@app.route('/users/<d_id>', methods=['DELETE'])
def delete_user(d_id):
    return User.delete(d_id)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
