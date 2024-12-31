import sqlite3


def init_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS t_email_auto_reply (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            email_date TIMESTAMP NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    pass


def insert_reply_content(from_email, subject, email_date):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO t_email_auto_reply (from_email, subject, email_date,create_time) VALUES (?, ?, ?,datetime("now","localtime"))',
        (from_email, subject, email_date))
    conn.commit()
    cursor.close()
    conn.close()


def select_max_email_date():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT max(email_date) from t_email_auto_reply')
    data = cursor.fetchall()
    return data[0][0]
