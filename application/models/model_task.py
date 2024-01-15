from sqlalchemy import Column, INTEGER, String, ForeignKey, TEXT, TIME
from sqlalchemy.orm import relationship

from infrastructure.database.database import Base


class Task(Base):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
    time = Column(TIME, nullable=False)
    title = Column(TEXT, nullable=False)
    status = Column(INTEGER, nullable=False)
    priority = Column(String(15), nullable=False)
    color_priority = Column(String(15), nullable=True, default="#fff")
    #from_admin = Column(Boolean, default=False)
    shedule_id = Column(INTEGER, ForeignKey("shedule.id"))
    shedule = relationship('Shedule', back_populates='task')
