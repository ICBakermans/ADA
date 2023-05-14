import os

from flask import Flask, request

from db import Base, engine
from resources.user import User
from resources.order import Order

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


@app.route('/users/<u_id>', methods=['PUT'])
def update_user(u_id):
    req_data = request.get_json()
    return User.update(u_id, req_data)


@app.route('/users/<u_id>', methods=['DELETE'])
def delete_user(u_id):
    return User.delete(u_id)

@app.route('/orders', methods=['POST'])
def create_order():
    req_data = request.get_json()
    return Order.create(req_data)

@app.route('/orders/<o_id>', methods=['PUT'])
def update_order(o_id):
    req_data = request.get_json()
    return Order.update(o_id, req_data)

@app.route('/orders/<o_id>', methods=['DELETE'])
def delete(o_id):
    return Order.delete(o_id)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
