# from app.core.database import Base
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
#
#
# class Todos(Base):
#     __tablename__: str = 'todos'
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     priority = Column(Integer)
#     description = Column(String)
#     complete = Column(Boolean, default=False)
#     owner_id = Column(Integer, ForeignKey('users.id'))
#
#
# class Users(Base):
#     __tablename__: str = 'users'
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True)
#     username = Column(String, unique=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#     role = Column(String)
