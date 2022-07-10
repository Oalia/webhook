from db import db as DB
from mql5python import mq5_python as mq
import strategies as ST


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
    "It was a sell signal entry so we register it's buy close using it original sell entry signal"
    closed = mq.close_all(sym, strategy_name)
    retry_close = 0
    while (not closed):
        if retry_close >= 3:
            break
        closed = mq.close_all(sym, strategy_name)
        retry_close = retry_close + 1
    if closed:
        DB.register_closed(sym, ST.SELL, strategy_name)

    retries = 0
    order = mq.order_buy(sym, strategy_name)
    while(not order):
        if retries >= 3:
            break
        order = mq.order_buy(sym, strategy_name)
        retries = retries + 1
    if order:    
        DB.register_opened_without_listening(sym, ST.BUY, strategy_name)


def half_cycle_sell(sym, strategy_name):
    closed = mq.close_all(sym, strategy_name)
    retry_close = 0
    while (not closed):
        if retry_close >= 3:
            break
        closed = mq.close_all(sym, strategy_name)
        retry_close = retry_close + 1
    if closed:
        DB.register_closed(sym, ST.SELL, strategy_name)

    retries = 0
    order = mq.order_sell(sym, strategy_name)
    while(not order):
        if retries >= 3:
            break
        order = mq.order_sell(sym, strategy_name)
        retries = retries + 1
    if order:    
        DB.register_opened_without_listening(sym, ST.SELL, strategy_name)


def cycle_buy(sym, strategy_name):
    closed = mq.close_all(sym, strategy_name)
    retry_close = 0
    while (not closed):
        if retry_close >= 3:
            break
        closed = mq.close_all(sym, strategy_name)
        retry_close = retry_close + 1
    if closed:
        DB.register_closed(sym, ST.SELL, strategy_name)

    retries = 0
    order = mq.order_buy(sym, strategy_name)
    while(not order):
        if retries >= 3:
            break
        order = mq.order_buy(sym, strategy_name)
        retries = retries + 1
    if order:    
        DB.register_opened(sym, ST.BUY, strategy_name)


def cycle_sell(sym, strategy_name):
    closed = mq.close_all(sym, strategy_name)
    retry_close = 0
    while (not closed):
        if retry_close >= 3:
            break
        closed = mq.close_all(sym, strategy_name)
        retry_close = retry_close + 1
    if closed:
        DB.register_closed(sym, ST.SELL, strategy_name)

    retries = 0
    order = mq.order_sell(sym, strategy_name)
    while(not order):
        if retries >= 3:
            break
        order = mq.order_sell(sym, strategy_name)
        retries = retries + 1
    if order:    
        DB.register_opened(sym, ST.SELL, strategy_name)