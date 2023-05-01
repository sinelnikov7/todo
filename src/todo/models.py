from sqlalchemy import Column, INTEGER, String, MetaData, Boolean, ForeignKey, DATE
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship
from auth.models import Base

class Shedule(Base):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
    data = Column(DATE)
