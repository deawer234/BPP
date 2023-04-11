from website.database.database import session
from website.model.movement_model import Movement
from website.model.position_model import Position

def add_positon(tab_id, position):
    session.add(Position(movement_id=tab_id, base=position['base'], shoulder=position['shoulder'], elbow=position['elbow'], wrist=position['wrist'], wrist_rot=position['wrist_rot'], gripper=position['gripper']))
    session.commit()


def remove_position(tab_id, position_id):
    position_to_delete = Position.query.where(Position.position_id == position_id and Position.movement_id == tab_id).first()
    session.delete(position_to_delete)
    session.commit()

def add_tab(name):
    session.add(Movement(name=name))
    session.commit()

def remove_tab(tab_id):
    tab_to_delete = Movement.query.where(Movement.movement_id == tab_id)
    session.delete(tab_to_delete)
    session.commit()

def get_tabs_with_positions():
    return Movement.query.join(Position).where(Position.movement_id != None).all()

def get_positions_of_tab(tab_id):
    return Position.query.where(Position.movement_id == tab_id).all()

def get_tabs():
    return Movement.query.all()