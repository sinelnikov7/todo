from sqlalchemy import Column, INTEGER, String, ForeignKey, DATE, TEXT, UniqueConstraint, TIME
from sqlalchemy.orm import relationship

from src.database import Base


class Shedule(Base):
    __tablename__ = 'shedule'
    id = Column(INTEGER, primary_key=True)
    date = Column(DATE)
    user_id = Column(INTEGER, ForeignKey("users.id"))
    user = relationship('User', back_populates='shedule')
    task = relationship('Task', back_populates='shedule', uselist=True)
    __table_args__ = (UniqueConstraint('date', 'user_id'),)


class Task(Base):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
    time = Column(TIME, nullable=False)
    title = Column(TEXT, nullable=False)
    status = Column(INTEGER, nullable=False)
    priority = Column(String(15), nullable=False)
    color_priority = Column(String(15), nullable=True, default="#fff")
    shedule_id = Column(INTEGER, ForeignKey("shedule.id"))
    shedule = relationship('Shedule', back_populates='task')


