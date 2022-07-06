from db  import db as DB
from mql5python import mq5_python as mq
import datetime
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

def hedge(sym, dir):
    "implement hedging strategy"

def update_depth(sym, id, depth):
    """"""
    
def enter_half_cycle(sym, dir, size, strategy_type):
    ""
    # enter first position, get it's db id, update its depth when other positions get filled
    ## hedging would probably rely on information from looking and analyzing past trade drawdowns in relation to itself, surroundings and outside forces
    ## hedging - like an insurance or like an opportunistic trade? which approach?
    ## as hedging in this case looks at the opposite direction, 
    # #is our trade and our current position an insurance or an opportunity?
    hedge(sym, dir)
    if strategy_type == "minus_step_one_buy":
        a = mq.order_buy(sym, size, half_id)
        b = mq.order_buy(sym, size, half_id)
        c = mq.order_sell(sym, size, quater_id)
        if a != None and b != None and c != None:
            DB.register_new_trade(sym,dir, b, created=datetime.time())
        else:
            print("ENTRY HALF CYCLE TRADE FAILED: ",a, b, c)

def close_half_cycle(sym, dir, strategy_type):
    # check if any trade remains and close it.

    if strategy_type == "minus_step_one_buy":
        mq.close_all()
    DB.register_closing_position(sym, dir)


def halving_event(sym, size, strategy_type):
    # if DB.check_halving(sym) == 0:
    if strategy_type == "minus_step_one_buy":
        mq.order_buy(sym, size, half_id)
        mq.order_sell(sym, size/4, half_id)
        mq.order_close_by_magic(sym, quater_id)
        DB.record_halving(sym)


# def close_first_step(dir, sym):
#     """"""

# def close_second_step(dir, sym):
#     """"""

# def shift_stoploss(dir, sym, step, entry_price):
#     """
#     calculations for shifting stop loss
    
#     """

    
# def update_position(dir, sym, step, entry_price):
#     if step == 0:
#         close_first_step(dir, sym)
#     if step == 1:
#         close_second_step(dir, sym)
#     else:
#         shift_stoploss(dir, sym, step, entry_price)

#     DB.update_step(sym,dir)