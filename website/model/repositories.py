from database.database import get_connection

conn = get_connection()

def add_positon(tab_id, position):
    data = (tab_id, position['shoulder'], position['elbow'], position['wrist'], position['wrist_rot'], position['gripper'])
    conn.execute('''INSERT INTO position (movement_id, shoulder, elbow, wrist, wrist_rot, gripper) VALUES(?, ?, ?, ?, ?, ?)''', data)
    return True


def remove_position(tab_id, position_id):
    data = (position_id, tab_id)
    query = ''' DELETE FROM position WHERE id = ? AND movement_id = ? '''
    conn.execute(query, data)
    return True

def add_tab(tab_id, name):
    data = (tab_id, name)
    query = ''' INSERT INTO movement (name) VALUES(?, ?) '''
    conn.execute(query, data)
    return True

def remove_tab(tab_id):
    data = tab_id
    query = ''' DELETE FROM movement WHERE id = ? '''
    conn.execute(query, data)
    return True

def get_positions_of_tab(tab_id):
    data = tab_id
    query = ''' SELECT * FROM position p INNER JOIN movement ON p.movement_id = ? '''
    return conn.execute(query, data)

def get_tabs():
    query = ''' SELECT * FROM movement'''
    return conn.execute(query)