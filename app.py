from datetime import datetime
from time import time
from timeit import timeit
from flask import Flask, request, abort, render_template
from numpy import double
from db import db as DB
import td as TD
from mql5python import mq5_python as mq
import strategies as ST



app = Flask(__name__)


@app.route('/')
def index():
    conn = DB.get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

def critical_error(str):
    print(str)

def strategy_step(sym, signal, type):
    strategy_name = ST.minus_step
    if type == "big":
        current_trade = DB.get_current_trade(sym, strategy_name)
        if current_trade != None:
                cur_dir = current_trade['signal']
                if cur_dir == signal: # if trade direction has changed.
                    if str(current_trade['opened']) == TD.TRADE_NOT_OPENED:
                        # TODO: 
                        critical_error("trade not placed amidst direction change") 
                    else:
                        if signal == ST.BUY:
                            print("st: heading to sells")
                            TD.half_cycle_sell(sym, strategy_name)
                        elif signal == ST.SELL:
                            print("st: heading to buys")
                            TD.half_cycle_buy(sym, strategy_name)
                else:
                    print("st: alarm, HODL, hedge? do nothing for now, HODL, smile, trust the process hahaha, don't get wrecked, touch some, get some")
        else:
            if signal == ST.BUY:
                print("st: heading to sells")
                TD.half_cycle_sell(sym, strategy_name)
            elif signal == ST.SELL:
                print("st: heading to buys")
                TD.half_cycle_buy(sym, strategy_name)  

def strategy_chill(sym, signal, type):
    strategy_name = ST.chill_a_little
    if type == "big":
        current_trade = DB.get_current_trade(sym, strategy_name)
        if current_trade != None:
                cur_dir = current_trade['signal']
                if cur_dir == signal: # if trade direction has changed.
                    if str(current_trade['opened']) == TD.TRADE_NOT_OPENED:
                        # TODO: 
                        critical_error("trade not placed amidst direction change") 
                    else:
                        if signal == ST.BUY:
                            print("ch: listening for sells")
                            DB.listen_for(ST.SELL, sym, strategy_name)
                        elif signal == ST.SELL:
                            print("ch: listening for buys")
                            DB.listen_for(ST.BUY, sym, strategy_name)
                else:
                    print("ch: do nothing for now")
        else:
            if signal == ST.BUY:
                print("ch: listening for sells")
                DB.listen_for(ST.SELL, sym, strategy_name)
            elif signal == ST.SELL:
                print("ch: listening for buys")
                DB.listen_for(ST.BUY, sym, strategy_name)
                
    elif type == "small":
        current_trade = DB.get_current_trade(sym, strategy_name)
        if current_trade != None:
            placed = current_trade["opened"]
            
            if placed == TD.TRADE_NOT_OPENED:
                cur_dir = current_trade['signal']
                if cur_dir == signal:
                    if signal == ST.BUY:
                        print("ch: confirmed for buys")
                        TD.cycle_buy(sym, strategy_name)
                    elif signal == ST.SELL:
                        print("ch: confirmed for sells")
                        TD.cycle_sell(sym, strategy_name)
            else: 
                print("ch: trade already placed.")


@app.route('/webhooks', methods=['POST'])
def webhook():
    webhook_message = (request.data)
    msg = webhook_message.decode(encoding='UTF-8').split(" ")
    type = msg[2]
    sym = msg[1]
    signal = msg[0]

    lg = ST.login_details(ST.minus_step)
    print("step")
    mq.initialize(login=lg['name'], server=lg['server'], password=lg['key'])
    strategy_step(sym, signal, type)
    mq.shutdown()

    lg = ST.login_details(ST.chill_a_little)
    print("chill")
    mq.initialize(login=lg['name'], server=lg['server'], password=lg['key'])
    strategy_chill(sym, signal, type)
    mq.shutdown()
    return ""

if __name__ == '__main__':
    app.run(debug=True, port=5000)