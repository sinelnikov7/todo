from sqlalchemy import Column, INTEGER, String, MetaData, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    activate = Column(Boolean, default=False)
    code = relationship('Code', back_populates="user", uselist=False)

class Code(Base):
    __tablename__ = 'codes'
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("users.id"))
    key = Column(INTEGER)
    user = relationship('User', back_populates='code')