"""
Model representing movement in database

Author: Daniel Němec
Date: 10.04.2023

Python Version: 3.8.10
"""

from website.database.database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Movement(Base):
    __tablename__ = 'Movement'
    movement_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    positions = relationship('Position', backref='Movement', cascade='all,delete', lazy=True)