from datetime import datetime
from time import time
from timeit import timeit
from flask import Flask, request, abort, render_template
from numpy import double
from db import db as DB
import td as TD
from mql5python import mq5_python as mq
app = Flask(__name__)

TRADE_NOT_CLOSED = 0
TRADE_IS_CLOSED = 1
TRADE_NOT_PLACED = 0
TRADE_PLACED =1 
@app.route('/')
def index():
    conn = DB.get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

def strategy_minus_step_one_buy(sym,dir,size,type):
    strategy_name = "minus_step_one_buy"
    if type == "big":
        current_trade = DB.get_current_trade(sym)
        if current_trade != None: #if a trade is open
            if current_trade['is_trade_closed'] == 0: 
                cur_dir = current_trade['dir']
                if cur_dir != dir: # if trade direction has changed.
                    print("TRYING TO CLOSE HALF CYCLE:\n")
                    TD.close_half_cycle(sym, dir, strategy_name)
                else:
                    print("ABOUT TO STEP FORWARD: WEAR YOUR SEATBELTS\n")
                    DB.update_step(sym, dir)
            elif current_trade['is_trade_closed'] == 1: 
                if dir == "DN":
                    print("NO OPEN TRADES ON KNOWN SYMBOL. ENTERING.\n")
                    TD.enter_half_cycle(sym, dir, size, strategy_name)
        else:
            if dir == "DN":
                print("NO CURRENT TRADE: START THE MACHINE:\n")
                TD.enter_half_cycle(sym, dir, size, strategy_name)
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
                        TD.halving_event(sym, size, strategy_name)

def critical_error(str):
    print(str)

def strategy_minus_step_one_buy_chill(sym,dir,size,type):
    strategy_name = "minus_chill"
    path_to_db = "db/{0}.db".format(strategy_name)
    if type == "big":
        current_trade = DB.get_current_trade(sym, path_to_db)
        if current_trade != None:
                cur_dir = current_trade['bias']
                if cur_dir != dir: # if trade direction has changed.
                    if current_trade['is_trade_placed'] == TRADE_NOT_PLACED:
                        # TODO: 
                        critical_error("trade not placed amidst direction change")
                        return 
                    else:
                        if dir == "DN":
                            DB.listen_for_buys(sym, path_to_db)
                        elif dir == "UP":
                            DB.listen_for_sells(sym, path_to_db)
                else:
                    "do nothing for now"
        else:
            if dir == "DN":
                DB.listen_for("UP", sym, path_to_db)
            elif dir == "UP":
                DB.listen_for("DN", sym, path_to_db)
                
    if type == "small":
        current_trade = DB.get_current_trade(sym, path_to_db)
        if current_trade != None:
            placed = current_trade["is_trade_placed"]
            
            if placed != TRADE_PLACED:
                cur_dir = current_trade['bias']
                if cur_dir == dir:
                    if dir == "UP":
                        TD.full_cycle_buy(sym, path_to_db)
                    elif dir == "DN":
                        TD.full_cycle_sell(sym, path_to_db)


@app.route('/webhooks', methods=['POST'])
def webhook():
    webhook_message = (request.data)
    msg = webhook_message.decode(encoding='UTF-8').split(" ")
    type = msg[3]
    dir = msg[0]
    sym = "AUDCHF"
    size = double(msg[1])/10
    mq.initialize()
    strategy_minus_step_one_buy(sym,dir,size,type)
    strategy_minus_step_one_buy_chill(sym,dir,size,type)
    
    mq.shutdown()
    return ""

if __name__ == '__main__':
    app.run(debug=True, port=5000)