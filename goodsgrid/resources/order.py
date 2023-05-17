from datetime import datetime

from flask import jsonify

from daos.order_dao import OrderDAO
from db import Session


class Order:
    @staticmethod
    def create(body):
        session = Session()
        
        # create order
        order = OrderDAO(body['product_id'], body['user_id'], body['payment_id'], body['shipping_id'], body['status'], datetime.now())
        session.add(order)
        session.commit()
        session.refresh(order)
        session.close()
        return jsonify({'order_id': order.id}), 200
    
    @staticmethod
    def update(o_id, body):
        session = Session()
        
        order = session.query(OrderDAO).filter(OrderDAO.id == o_id).first()

        if order is not None:
            #Check which parameters are set
            if 'status' in body:
                order.status = body['status']
                order.last_update = datetime.now()


            #Update user
            session.commit()
            return jsonify({'message': 'The order is updated succesfully.'}), 200
        else:
            return jsonify({'message': 'This user does not exists'}), 400
    
    @staticmethod
    def delete(o_id):
        session = Session()
        effected_rows = session.query(OrderDAO).filter(OrderDAO.id == o_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no order with id {o_id}'}), 404
        else:
            return jsonify({'message': f'The order with id {o_id} was removed'}), 200


