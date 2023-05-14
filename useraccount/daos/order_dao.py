from sqlalchemy import Column, String, Integer, DateTime 

from db import Base


class OrderDAO(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    product_id = Column(Integer)
    user_id = Column(Integer)
    payment_id = Column(Integer)
    shipping_id = Column(Integer)
    status = Column(String)
    last_update = Column(DateTime)


    def __init__(self, product_id, user_id, payment_id ,shipping_id, status, last_update):
        self.product_id = product_id
        self.user_id = user_id
        self.payment_id = payment_id
        self.shipping_id = shipping_id
        self.status = status
        self.last_update = last_update