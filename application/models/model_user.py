import datetime

from sqlalchemy import Column, INTEGER, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import  relationship

from infrastructure.database.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    activate = Column(Boolean, default=False)
    data_create = Column(Date, nullable=True, default=None)
    is_admin = Column(Boolean, default=False)
    code = relationship('Code', back_populates="user", uselist=False)
    shedule = relationship('Shedule', back_populates="user")
    admin_id = Column(INTEGER, ForeignKey("users.id"))
    #admin = relationship('User', back_populates='admin')



class Code(Base):
    __tablename__ = 'codes'
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("users.id"))
    key = Column(INTEGER)
    user = relationship('User', back_populates='code')
