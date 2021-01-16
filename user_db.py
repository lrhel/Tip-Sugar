import sqlite3
import time

import config

def db_init():
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    create_table = '''CREATE TABLE IF NOT EXISTS userlist(user_id TEXT, name TEXT, last_claimed INTEGER)'''
    cur.execute(create_table)
    create_table = '''CREATE TABLE IF NOT EXISTS prefix(server INTEGER, prefix TEXT)'''
    cur.execute(create_table)

def add_user(user_id, name):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    sql = 'INSERT INTO userlist (user_id, name, last_claimed) VALUES (?,?,0)'
    user = (user_id, name)
    cur.execute(sql, user)
    con.commit()
    con.close()

def check_user(id):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM userlist WHERE user_id = ?', (str(id),))
    if cur.fetchall() == []:
        return False
    else:
        return True

def add_prefix(server, prefix):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    sql = 'DELETE FROM prefix WHERE server = ?'
    cur.execute(sql,(server,))
    sql = 'INSERT INTO prefix VALUES (:s,:l),(:s,:c)'
    cur.execute(sql,{"s":server,"l":prefix.lower(),"c":prefix.capitalize()})
    con.commit()
    con.close()

def get_prefix(server):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    sql = 'SELECT prefix FROM prefix WHERE server = ?'
    cur.execute(sql,(server,))
    res = cur.fetchall()
    return res[0] if res else None

def can_claim(id):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    cur.execute('SELECT last_claimed FROM userlist WHERE user_id = ?', (str(id),))
    res = cur.fetchall()
    return (res[0][0] + config.faucet_time < int(time.time()), res[0][0])

def update_claim(id):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    cur.execute('UPDATE userlist SET last_claimed = ? WHERE user_id = ?', (int(time.time()),str(id)))
    con.commit()
    con.close()
