import sqlite3

connection = sqlite3.connect('database.db')

"""
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dir TEXT NOT NULL,
    sym TEXT NOT NULL,
    step int NOT NULL,
    depth int NOT NULL,
    entry_price real NOT NULL,
);
"""
with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()
cur.execute("INSERT INTO posts (id, created, dir, sym, step, depth, entry_price) VALUES (?,?,?,?,?,?,?)",
            ('First Post', 'Content for the first post')
            )
connection.commit()
connection.close()
