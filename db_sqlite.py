import os
import sqlite3 as sqlite

import constants


def _execute(query, param=None):
    connection = sqlite.connect(constants.DB_NAME)
    cursorobj = connection.cursor()
    try:
        if param:
            cursorobj.execute(query, param)
        else:
            cursorobj.execute(query)
        result = cursorobj.lastrowid if query.startswith('INSERT') else cursorobj.fetchall()
        connection.commit()
    except Exception:
        raise
    connection.close()
    return result


def init_database():
    if os.path.exists(constants.DB_NAME):
        os.remove(constants.DB_NAME)
    _execute(
        '''
        CREATE TABLE IF NOT EXISTS tenants (
            id INTEGER PRIMARY KEY autoincrement,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            arrival TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            departure TIMESTAMP DEFAULT NULL,
            room_number INTEGER NOT NULL
        )
        '''
    )
