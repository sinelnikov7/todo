from sqlalchemy import Column, INTEGER, ForeignKey, DATE, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Column, INTEGER, String, ForeignKey, TEXT, TIME

from application.models.model_task import Task
from infrastructure.database.database import Base


class Shedule(Base):
    __tablename__ = 'shedule'
    id = Column(INTEGER, primary_key=True)
    date = Column(DATE)
    user_id = Column(INTEGER, ForeignKey("users.id"))
    user = relationship('User', back_populates='shedule')
    task = relationship('Task', back_populates='shedule', uselist=True)
    __table_args__ = (UniqueConstraint('date', 'user_id'),)

