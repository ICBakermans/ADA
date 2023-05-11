from datetime import datetime

from flask import jsonify

from daos.user_dao import UserDAO
from db import Session


class User:
    @staticmethod
    def create(body):
        session = Session()
        
        # check if email already exists
        existing_user = session.query(UserDAO).filter(UserDAO.email == body['email']).first()
        if existing_user is not None:
            session.close()
            return jsonify({'message': 'Email already exists'}), 409
        
        # check if username already exists
        existing_user = session.query(UserDAO).filter(UserDAO.username == body['username']).first()
        if existing_user is not None:
            session.close()
            return jsonify({'message': 'Username already exists'}), 409
        
        # create user
        user = UserDAO(body['first_name'], body['last_name'], body['email'], body['username'], body['password'],body['user_role'])
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return jsonify({'user_id': user.id}), 200

    @staticmethod
    def delete(u_id):
        session = Session()
        effected_rows = session.query(UserDAO).filter(UserDAO.id == u_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no user with id {u_id}'}), 404
        else:
            return jsonify({'message': f'The user with id {u_id} was removed'}), 200
        
    @staticmethod
    def update(u_id, body):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.id == u_id).first()

        if user is not None:
            #Check which parameters are set
            if 'first_name' in body:
                user.first_name = body['first_name']
            if 'last_name' in body:
                user.last_name = body['last_name']
            if 'email' in body:
                user.email = body['email']
            if 'username' in body:
                user.username = body['username']
            if 'user_role' in body:
                user.user_role = body['user_role']

            #Update user
            session.commit()
            return jsonify({'message': 'The user is updated succesfully.'}), 200
        else:
            return jsonify({'message': 'This user does not exists'}), 400

    
    @staticmethod
    def authenticate(body):
        session = Session()

        if 'username' in body and 'password' in body:
            user = session.query(UserDAO).filter(UserDAO.username == body['username']).first()
            if user is not None and user.password == body['password']:
                session.close()
                return jsonify({'user_id': user.id}), 200
            else:
                session.close()
                return jsonify({'message': 'Invalid credentials'}), 401
        else:
            session.close()
            return jsonify({'message': 'Missing username or password'}), 400

