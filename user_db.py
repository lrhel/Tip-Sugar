import sqlite3

def db_init():
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    create_table = '''CREATE TABLE IF NOT EXISTS userlist(user_id TEXT, name TEXT)'''
    cur.execute(create_table)
    create_table = '''CREATE TABLE IF NOT EXISTS prefix(server INTEGER, prefix TEXT)'''
    cur.execute(create_table)

def add_user(user_id, name):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()

    sql = 'INSERT INTO userlist (user_id, name, 0, "") VALUES (?,?)'
    user = (user_id, name)
    cur.execute(sql, user)
    con.commit()
    con.close()

def check_user(id):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM userlist WHERE user_id={0}'.format(id))
    if cur.fetchall() == []:
        return False
    else:
        return True

def add_prefix(server, prefix):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    sql = 'DELETE FROM prefix WHERE server = ?'
    cur.execute(sql,(prefix,))
    sql = 'INSERT INTO prefix VALUES (:s,:l),(:s,:c)'
    cur.execute(sql,{"s":server,"l":prefix.lower(),"c":prefix.capitalize()})
    con.commit()
    con.close()

def get_prefix(server):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()
    sql = 'SELECT prefix FROM prefix WHERE server = ?'
    cur.execute(sql,(server,))
    return cur.fetchall()[0] if cur.fetchall() else None

