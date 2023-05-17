from sqlalchemy import Column, String, Integer

from db import Base


class UserDAO(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    user_role = Column(String)


    def __init__(self, first_name, last_name, email ,username, password, user_role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.user_role = user_role
