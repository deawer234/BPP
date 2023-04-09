from database.database import get_connection

def add_positon(tab_id, position):
    conn = get_connection("../database/db.db")
    data = (tab_id, position['shoulder'], position['elbow'], position['wrist'], position['wrist_rot'], position['gripper'])
    conn.execute('''INSERT INTO position(movement_id, shoulder, elbow, wrist, wrist_rot, gripper) VALUES(?, ?, ?, ?, ?, ?)''', data)



def remove_position(tab_id, position_id):
    return 
def add_tab(tab_id, name):
    return 
def remove_tab(tab_id):
    return