import sqlite3


def init_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS t_cos_file (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_key TEXT NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    pass


def insert_wait_delete_file(file_key):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(
        'DELETE from t_cos_file where file_key = ?', (file_key,))
    cursor.execute(
        'INSERT INTO t_cos_file (file_key,create_time) VALUES (?,datetime("now","localtime"))',(file_key,))
    conn.commit()
    cursor.close()
    conn.close()


def select_wait_delete_file():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id,file_key from t_cos_file where create_time < datetime("now","-1 hour","localtime")')
    data = cursor.fetchall()
    return data  # [(1, 'file_key'), (2, 'file_key')]


def delete_file(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('delete from t_cos_file where id =?', (id,))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if len(data) == 0:
        return True
    return data[0][0]
