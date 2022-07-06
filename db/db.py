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
    is_trade_closed TEXT
);
"""
def create_table(conn, table_name):
    with open('db/schema.sql') as f:
        conn.executescript(f.read())
    conn.execute(f'ALTER TABLE posts RENAME TO {table_name}')   
    return conn

def check_if_table_exists_create_one_if_not(table_name, db_path): 
    conn = get_db_connection(db_path)
    conn.row_factory = sqlite3.Row   #   add this row
    c = conn.cursor()
    c.execute(f'SELECT count(name) FROM sqlite_master WHERE type="table" AND name=\'{table_name}\';')
    # print(i)
    if c.fetchone()[0] == 1:
        return conn
    else:
        return create_table(conn, table_name)
        
'db/database.db'
def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# if same trade dir, we could update stop losses or take partial credit if step 1. If not, we exit. 
# Enter new set of trades. and register those trades.
def get_current_trade(symbol, db_path):
    conn = check_if_table_exists_create_one_if_not(symbol, db_path)
    conn.row_factory = sqlite3.Row   #   add this row
    position = conn.execute(f'SELECT * FROM {symbol} order by ID DESC LIMIT 1').fetchone()
    return position

def register_new_trade(sym, dir, entry_price, created, db_path):
    conn = check_if_table_exists_create_one_if_not(sym, db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO {0} (created, dir, sym, step,halving, entry_price, is_trade_closed) VALUES (?,?,?,?,?,?,?)".format(str(sym)),
                (str(created), str(dir), str(sym), str(0), str(0), str(entry_price), str(0))
                )
    conn.commit()
    conn.close()

def register_closing_position(sym, dir, db_path):
    symbol_table = get_current_trade(sym, db_path)
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    x=curr.execute('''select MAX(ID) from {0};'''.format(sym))
    id=x.fetchone()[0]
    s = '''UPDATE {0} 
            SET is_trade_closed={1} 
            WHERE ID={2}'''.format(symbol_table['sym'], 1, str(id))
    print(s)
    curr.execute(s)
    conn.commit()
    conn.close()
            

def update_step(sym, dir, db_path):
    symbol_table = get_current_trade(sym, db_path)
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    x=curr.execute('''select MAX(ID) from {0};'''.format(sym))
    id=x.fetchone()[0]
    s = '''UPDATE {0} 
            SET step={1} 
            WHERE ID={2}'''.format(symbol_table['sym'], int(symbol_table['step'])+1, str(id))
    print(s)
    curr.execute(s)
    conn.commit()
    conn.close()

def record_halving(sym, db_path):
    symbol_table = get_current_trade(sym, db_path)
    conn = get_db_connection(db_path)
    halving = 1
    curr = conn.cursor()
    x=curr.execute('''select MAX(ID) from {0};'''.format(sym))    
    id=x.fetchone()[0]
    curr.execute('UPDATE {0} SET halving = ? WHERE id =? AND dir = ?'.format(str(symbol_table['sym'])), (str(halving), str(id), str(dir)))
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