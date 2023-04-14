from website.database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Movement(Base):
    __tablename__ = 'Movement'
    movement_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    positions = relationship('Position', backref='Movement', cascade='all,delete', lazy=True)