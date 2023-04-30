from sqlalchemy import Column, INTEGER, String, MetaData, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship
from auth.models import Base


class Task(Base):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
