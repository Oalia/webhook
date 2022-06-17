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
);
"""
def check_if_table_exists_create_one_if_not(table_name):
    conn = get_db_connection()
    i = conn.execute(f'SELECT count(*) FROM sqlite_master WHERE type="table" AND name={table_name};')
    if i == 1:
        return conn
    else:
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.execute(f'ALTER TABLE posts RENAME TO {table_name}')   
        return conn

def get_db_connection():
    conn = sqlite3.connect('webhook/db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


# if same trade dir, we could update stop losses or take partial credit if step 1. If not, we exit. 
# Enter new set of trades. and register those trades.
def get_current_trade(symbol):
    conn = check_if_table_exists_create_one_if_not(symbol)
    position = conn.execute(f'SELECT * FROM {symbol} WHERE id = (SELECT LAST_INSERT_ID())').fetchone()
    return position

def register_new_trade(sym, dir, depth, entry_price):
    conn = check_if_table_exists_create_one_if_not(sym)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {sym} (sym, dir, depth, entry_price, status) VALUES (?, ?, ?, ?, ?)",
                (f'{sym}', f'{dir}', f'{depth}', f'{entry_price}', 'open')
                )
    # conn.close()

# register_closing_position(sym, status = "closed")
def register_closing_position(sym, dir):
    symbol_table = get_current_trade(sym)
    conn = get_db_connection()
    conn.execute('UPDATE {symbol_table} SET status = closed'
                    ' WHERE id = (SELECT LAST_INSERT_ID()) AND dir = ?', (dir))
    conn.commit()
    # conn.close()
            

def update_step(sym, dir):
    symbol_table = get_current_trade(sym)
    conn = get_db_connection()
    next_step = symbol_table['step']+1
    conn.execute('UPDATE {symbol_table} SET step = ?'
                    ' WHERE id = (SELECT LAST_INSERT_ID()) AND dir = ?', (next_step, dir))
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