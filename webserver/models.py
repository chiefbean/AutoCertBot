import sqlite3 as sql
import bcrypt

def verify(username, password):
    con = sql.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    for user in users:
        if user[0] == username and bcrypt.checkpw(password.encode(), user[1]):
            return True
    return False

def changePass(username, password):
    salt = bcrypt.gensalt()
    pass_hash = bcrypt.hashpw(password.encode(), salt)
    con = sql.connect("db.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET password = ? WHERE username = ?", (pass_hash, username))
    con.commit()
    con.close()
    return False