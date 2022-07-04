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
    # time_entry = datetime.now()
    webhook_message = (request.data)
    msg = webhook_message.decode(encoding='UTF-8').split(" ")
    type = msg[3]
    dir = msg[0]
    sym = msg[2]
    size = double(msg[1])

    """
    THIS SIMPLE:   
    will be getting entry and exit xignals alone.
    updates would incorporate, drawdowns, hedging, and possible tracking/updatiing by continual step signals
    """
    if type == "big":
        current_trade = DB.get_current_trade(sym)
        if current_trade != None: #if a trade is open
            if current_trade['open'] == True:
                cur_dir = current_trade['dir']
                if cur_dir != dir: # if trade direction has changed.
                    TD.close_half_cycle(sym, dir, "minus_step_one_buy")
                else:
                    DB.update_step(sym, dir)
            elif current_trade['open'] == False:
                if dir == "DN":
                    TD.enter_half_cycle(sym, dir, size, "minus_step_one_buy")
        else:
            if dir == "DN":
                TD.enter_half_cycle(sym, dir, size, "minus_step_one_buy")
        
    if type == "small":
        current_trade = DB.get_current_trade(sym)
        if current_trade != None: #if a trade is open
            step = current_trade['step']
            if step >= 2:
                cur_dir = current_trade['dir']
                if cur_dir != dir: #
                    if current_trade['halving'] == False:
                        TD.halving_event(sym, size, "minus_step_one_buy")
    return ""

if __name__ == '__main__':
    app.run(debug=True, port=3000)
