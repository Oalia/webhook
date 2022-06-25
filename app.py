from datetime import datetime
from time import time
from timeit import timeit
from flask import Flask, request, abort, render_template
from numpy import double
from db import db as DB
import td as TD

app = Flask(__name__)


@app.route('/')
def index():
    conn = DB.get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


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
@app.route('/webhooks', methods=['POST'])
def webhook():
    """
    Example Message: DN 50 UK100
    """
    time_entry = datetime.now()
    webhook_message = (request.data)
    msg = webhook_message.decode(encoding='UTF-8').split(" ")
    dir = msg[0]
    sym = msg[2]
    size = double(msg[1])
    print(msg, dir, size)

    # close

    current_trade = DB.get_current_trade(sym)
    if current_trade != None:
        cur_dir = current_trade['dir']
        if cur_dir != dir:
            # TD.close_half_cycle(sym, dir, size, "minus_step_one_buy")
            # TD.enter_half_cycle(sym, dir, size, "minus_step_one_buy")

            DB.register_closing_position(sym, dir)
            # DB.register_new_trade(sym, dir, entry_price="", created=time_entry)
        
        else:
            # print(current_trade['step'])
            TD.update_position(dir, sym, current_trade['step'], current_trade['entry_price'])
    else:
        TD.enter_half_cycle(sym, dir, size, "minus_step_one_buy")
        
    return ""

if __name__ == '__main__':
    app.run(debug=True, port=3000)
