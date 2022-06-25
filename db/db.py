from flask import redirect, request, abort, render_template, flash, url_for
import json
import sqlite3
from numpy import double
import config

"""
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dir TEXT NOT NULL,
    sym TEXT NOT NULL,
    step int NOT NULL,
    depth int NOT NULL,
    entry_price real NOT NULL,
    status TEXT
);
"""
def create_table(conn, table_name):
    with open('webhook/db/schema.sql') as f:
            conn.executescript(f.read())
    conn.execute(f'ALTER TABLE posts RENAME TO {table_name}')   
    return conn

def check_if_table_exists_create_one_if_not(table_name):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row   #   add this row
    c = conn.cursor()
    c.execute(f'SELECT count(name) FROM sqlite_master WHERE type="table" AND name=\'{table_name}\';')
    # print(i)
    if c.fetchone()[0] == 1:
        return conn
    else:
        return create_table(conn, table_name)
        

def get_db_connection():
    conn = sqlite3.connect('webhook/db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


# if same trade dir, we could update stop losses or take partial credit if step 1. If not, we exit. 
# Enter new set of trades. and register those trades.
def get_current_trade(symbol):
    conn = check_if_table_exists_create_one_if_not(symbol)
    conn.row_factory = sqlite3.Row   #   add this row
    position = conn.execute(f'SELECT * FROM {symbol} order by ID DESC LIMIT 1').fetchone()
    return position

def register_new_trade(sym, dir, entry_price, created):
    conn = check_if_table_exists_create_one_if_not(sym)
    cur = conn.cursor()
    cur.execute("INSERT INTO {0} (created, dir, sym, step, entry_price, status) VALUES (?,?,?,?,?,?)".format(sym),
                (created, dir, sym, 0, entry_price, "open")
                )
    conn.commit()
    # conn.close()

# register_closing_position(sym, status = "closed")
def register_closing_position(sym, dir):
    symbol_table = get_current_trade(sym)
    conn = get_db_connection()
    conn.execute('UPDATE {0} SET status = closed'
                    ' WHERE id = (SELECT LAST_INSERT_ID()) AND dir = ?'.format(symbol_table), (dir))
    conn.commit()
    # conn.close()
            

def update_step(sym, dir):
    symbol_table = get_current_trade(sym)
    conn = get_db_connection()
    next_step = symbol_table['step']+1
    conn.execute('UPDATE {0} SET step = {1} WHERE id = (SELECT LAST_INSERT_ID()) AND dir = {2}'.format(symbol_table,next_step,dir))
    conn.commit()
    conn.close()

# def edit_trade(id):
#     post = get_current_trade(id)
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         if not title:
#             flash('Title is required!')

#         elif not content:
#             flash('Content is required!')
#         else:
#             conn = get_db_connection()
#             conn.execute('UPDATE {posts} SET title = ?, content = ?'
#                          ' WHERE id = ?',
#                          (title, content, id))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('index'))
#     return render_template('edit.html', post=post)