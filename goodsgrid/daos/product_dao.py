from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from db import Base


class ProductDAO(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    user_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    brand = Column(String)
    color = Column(String)
    size = Column(String)
    stock = Column(Integer)
    price = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, id, user_id, title, description, brand, color, size, stock,price, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.brand = brand
        self.color = color
        self.size = size
        self.stock = stock
        self.price = price
        self.created_at = created_at
        self.updated_at = updated_at