from website.database.database import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String

class Position(Base):
    __tablename__= 'Position'
    position_id = Column(String, primary_key=True)
    base = Column(Integer, nullable=False)
    shoulder = Column(Integer, nullable=False)
    elbow = Column(Integer, nullable=False)
    wrist = Column(Integer, nullable=False)
    wrist_rot = Column(Integer, nullable=False)
    gripper = Column(Integer, nullable=False)
    movement_id = Column(String, ForeignKey('Movement.movement_id'), nullable=False)
