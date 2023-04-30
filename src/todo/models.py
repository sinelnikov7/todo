from sqlalchemy import Column, INTEGER, String, MetaData, Boolean, ForeignKey, DATE
from sqlalchemy.orm import relationship
from database import Base


class Task(Base):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
    data = Column(DATE)
