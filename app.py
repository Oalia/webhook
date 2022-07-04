from datetime import datetime
from time import time
from timeit import timeit
from flask import Flask, request, abort, render_template
from numpy import double
from db import db as DB
import td as TD
from mql5python import mq5_python as mq
app = Flask(__name__)

@app.route('/')
def index():
    conn = DB.get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/webhooks', methods=['POST'])
def webhook():
    webhook_message = (request.data)
    msg = webhook_message.decode(encoding='UTF-8').split(" ")
    type = msg[3]
    dir = msg[0]
    sym = "AUDCHF"
    size = double(msg[1])/10
    mq.initialize()
    if type == "big":
        current_trade = DB.get_current_trade(sym)
        if current_trade != None: #if a trade is open
            if current_trade['order_status'] == 0: 
                cur_dir = current_trade['dir']
                if cur_dir != dir: # if trade direction has changed.
                    print("TRYING TO CLOSE HALF CYCLE:\n")
                    TD.close_half_cycle(sym, dir, "minus_step_one_buy")
                else:
                    print("ABOUT TO STEP FORWARD: WEAR YOUR SEATBELTS\n")
                    DB.update_step(sym, dir)
            elif current_trade['order_status'] == 1: 
                if dir == "DN":
                    print("NO OPEN TRADES ON KNOWN SYMBOL. ENTERING.\n")
                    TD.enter_half_cycle(sym, dir, size, "minus_step_one_buy")
        else:
            if dir == "DN":
                print("NO CURRENT TRADE: START THE MACHINE:\n")
                TD.enter_half_cycle(sym, dir, size, "minus_step_one_buy")
            if dir == "UP":
                print("dude")

    if type == "small":
        current_trade = DB.get_current_trade(sym)
        if current_trade != None: #if a trade is open
            step = current_trade['step']
            if step >= 2:
                cur_dir = current_trade['dir']
                if cur_dir != dir: #
                    if current_trade['halving'] == 0:
                        TD.halving_event(sym, size, "minus_step_one_buy")
    mq.shutdown()
    return ""

if __name__ == '__main__':
    app.run(debug=True, port=5000)