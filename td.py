import imp
from db import db as DB
from mql5python import mq5_python as mq
import strategies as ST
import util as UT

"""
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dir TEXT NOT NULL,
    sym TEXT NOT NULL,
    step int NOT NULL,
    size int NOT NULL,
    depth int NOT NULL,
    entry_price real NOT NULL,
    is_trade_closed TEXT NOT NULL,
);
"""


quater_id = 32
half_id = 321

TRADE_CLOSED = 1
TRADE_NOT_CLOSED = 0
TRADE_PLACED =1 
TRADE_NOT_PLACED = 0
TRADE_OPENED = 1
TRADE_NOT_OPENED = 0


def hedge(sym, dir):
    "implement hedging strategy"

def half_cycle_buy(sym, strategy_name):
    mq.close_positons_by_symbol(sym, strategy_name)
    DB.register_closed(sym, ST.BUY, strategy_name) 
    mq.order_buy(sym, strategy_name) 
    DB.register_opened_without_listening(sym, ST.BUY, strategy_name)
    # "It was a sell signal entry so we register it's buy close using it original sell entry signal"
    # for i in range(3):
    #     closed = mq.close_positons_by_symbol(sym, strategy_name)
    #     if closed == True:
    #         DB.register_closed(sym, ST.BUY, strategy_name)
    #         break
    #     if i == 2:
    #         UT.critical_error("NOT CLOSED HC BUY")
    # for i in range(3):
    #     order = mq.order_buy(sym, strategy_name)
    #     if(order==True):
    #         print("HCycle Buy Entered")
    #         DB.register_opened_without_listening(sym, ST.BUY, strategy_name)
    #         break


def half_cycle_sell(sym, strategy_name):
    mq.close_positons_by_symbol(sym, strategy_name) 
    DB.register_closed(sym, ST.SELL, strategy_name)
    mq.order_sell(sym, strategy_name)
    DB.register_opened_without_listening(sym, ST.SELL, strategy_name)
    # for i in range(3):
    #     closed = mq.close_positons_by_symbol(sym, strategy_name)
    #     if closed == True:
    #         DB.register_closed(sym, ST.SELL, strategy_name)
    #         break
    #     if i == 2:
    #         UT.critical_error("ORDER NOT CLOSED HALF CYCLE SELL")
    # for i in range(3):
    #     order = mq.order_sell(sym, strategy_name)
    #     if(order==True):
    #         print("HCycle Buy Entered")
    #         DB.register_opened_without_listening(sym, ST.SELL, strategy_name)
    #         break

def cycle_buy(sym, strategy_name):
    mq.close_positons_by_symbol(sym, strategy_name) 
    DB.register_closed(sym, ST.BUY, strategy_name) 
    mq.order_buy(sym, strategy_name) 
    DB.register_opened(sym, ST.BUY, strategy_name)
    # for i in range(3):
    #     closed = mq.close_positons_by_symbol(sym, strategy_name)
    #     if closed == True:
    #         DB.register_closed(sym, ST.BUY, strategy_name)
    #         break
    #     if i == 2:
    #         UT.critical_error("NOT CLOSED C BUY")
    # for i in range(3):
    #     order = mq.order_buy(sym, strategy_name)
    #     if(order==True):
    #         print("Cycle Buy Entered")
    #         DB.register_opened(sym, ST.BUY, strategy_name)
    #         break

def cycle_sell(sym, strategy_name):
    mq.close_positons_by_symbol(sym, strategy_name) 
    DB.register_closed(sym, ST.SELL, strategy_name) 
    mq.order_sell(sym, strategy_name) 
    DB.register_opened(sym, ST.SELL, strategy_name)
    # for i in range(3):
    #     closed = mq.close_positons_by_symbol(sym, strategy_name)
    #     if closed == True:
    #         DB.register_closed(sym, ST.SELL, strategy_name)
    #         break
    #     if i == 2:
    #         UT.critical_error("ORDER NOT CLOSED CYCLE SELL")
    # for i in range(3):
    #     order = mq.order_sell(sym, strategy_name)
    #     if(order==True):
    #         print("Cycle Buy Entered")
    #         DB.register_opened(sym, ST.SELL, strategy_name)
    #         break