import sqlite3

from bot.data import DbWaitVerifyFriend


def initTable():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # 创建 t_wait_verify_friend 表
    DbWaitVerifyFriend.init_table_t_wait_verify_friend(cursor)
    conn.commit()
    cursor.close()
    conn.close()