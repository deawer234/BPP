"""
Repositories for manipulation with data in database.

Author: Daniel Němec
Date: 15.03.2023

Python Version: 3.8.10
"""

from website.database.database import session
from website.model.movement_model import Movement
from website.model.position_model import Position

def add_positon(tab_id, position):
    session.add(Position(position_id=str(position['position_id']), base=int(position['base']), shoulder=int(position['shoulder']), elbow=int(position['elbow']), wrist=int(position['wrist']), wrist_rot=int(position['wrist_rot']), gripper=int(position['gripper']), movement_id=str(tab_id)))
    session.commit()


def remove_position(position_id):
    position_to_delete = Position.query.where(Position.position_id == str(position_id)).first()
    session.delete(position_to_delete)
    session.commit()

def add_tab(tab_id, name):
    session.add(Movement(movement_id=tab_id, name=name))
    session.commit()

def get_position(position_id):
    return Position.query.where(Position.position_id == str(position_id)).first()

def remove_tab(tab_id):
    print(tab_id)
    tab_to_delete = Movement.query.where(Movement.movement_id == str(tab_id)).first()
    session.delete(tab_to_delete)
    session.commit()

def get_positions_of_tab(tab_id):
    return Position.query.where(Position.movement_id == tab_id).all()

def get_tabs():
    return Movement.query.all()
