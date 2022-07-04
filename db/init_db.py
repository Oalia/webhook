import sqlite3
import time

connection = sqlite3.connect('db/database.db')

"""
CREATE TABLE posts (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dir TEXT NOT NULL,
    sym TEXT NOT NULL,
    step int NOT NULL,
    halving boolean NOT NULL,
    entry_price real NOT NULL,
    order_status TEXT 
);
"""
with open('db/schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()
# cur.execute("INSERT INTO posts (created, dir, sym, step, halving, entry_price, order_status) VALUES (?,?,?,?,?,?,?)",
#             (str(time.time()), str('test_dir'), str("test_symbol"), str("0"), str("0"), str("0.00"), str("0"))
#             )
connection.commit()
connection.close()
