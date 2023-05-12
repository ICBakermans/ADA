from datetime import datetime
from flask import jsonify
from inventory_service.daos.product_dao import ProductDAO
from inventory_service.db import Session

class Product:
    @staticmethod
    def create(body):
        session = Session()
        existing_product = session.query(ProductDAO).filter(ProductDAO.id == body['id']).first()
        if existing_product is not None:
            session.close()
            return jsonify({'message': 'Product already exists'}), 409
        product = ProductDAO(body['id'], body['user_id'], body['title'], body['description'], body['brand'],
                              body['color'], body['size'], body['stock'], body['price'], datetime.now(), datetime.now())
        session.add(product)
        session.commit()
        session.refresh(product)
        session.close()
        return jsonify({'Product created with id:': product.id}), 201

    @staticmethod
    def get(p_id):
        session = Session()
        product = session.query(ProductDAO).filter(ProductDAO.id == int(p_id)).first()
        if product:
            text_out = {
                "product_id:": product.id,
                "user_id": product.user_id,
                "title": product.title,
                "description": product.description,
                "brand": product.brand,
                "color": product.color,
                "size": product.size,
                "stock": product.stock,
                "price": product.price,
                "created_at": product.created_at.isoformat(),
                "updated_at": product.updated_at.isoformat(),
                }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no product with id {p_id}'}), 404

    @staticmethod
    def update_inventory(p_id, body):
        session = Session()
        product = session.query(ProductDAO).filter(ProductDAO.id == p_id).first()
        if product is not None:
            if 'stock' in body:
                product.stock = body['stock']
                session.commit()
                product.updated_at = datetime.now()
                session.commit()
                return jsonify({'message': f'The stock is successfully updated at {product.updated_at} and now is {product.stock}'}), 200
            else:
                return jsonify({'message': 'No updated stock amount was given'}), 400
        else:
            return jsonify({'message': 'This product does not exist'}), 404

    @staticmethod
    def check_stock(p_id):
        session = Session()
        product = session.query(ProductDAO).filter(ProductDAO.id == p_id).first()
        if product is not None:
            session.close()
            return jsonify({'stock': product.stock}), 200
        else:
            session.close()
            return jsonify({'message': 'This product does not exist'}), 404


    @staticmethod
    def accept_reject(p_id, body):
        session = Session()
        product = session.query(ProductDAO).filter(ProductDAO.id == p_id).first()
        if product is not None:
            if 'order_amount' in body:
                if product.stock >= body['order_amount']:
                    session.close()
                    return jsonify({'message': 'Accepted'}), 202
                else:
                    session.close()
                    return jsonify({'message': 'Rejected'}), 406
            else:
                session.close()
                return jsonify({'message': 'No order amount has been given'}), 400
        else:
            session.close()
            return jsonify({"This product does not exist"}), 404

    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(ProductDAO).filter(ProductDAO.id == int(d_id)).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no product with id {d_id}'}), 404
        else:
            return jsonify({'message': f'Product with id {d_id} was removed'}), 200
