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
    status TEXT NOT NULL,
);
"""

def hedge(sym, dir):
    "implement hedging strategy"

def update_depth(sym, id, depth):
    """"""
    
def enter_half_cycle(sym, dir, size, strategy_type):
    ""
    # enter first position, get it's db id, update its depth when other positions get filled
    depth = 0
    entry_price = 0
    ## hedging would probably rely on information from looking and analyzing past trade drawdowns in relation to itself, surroundings and outside forces
    ## hedging - like an insurance or like an opportunistic trade? which approach?
    ## as hedging in this case looks at the opposite direction, 
    # #is our trade and our current position an insurance or an opportunity?
    hedge(sym, dir)
    if strategy_type == "minus_step_one_buy":
        if dir == 1:
            mq.order_buy(sym, size)
        elif dir == 0:
            mq.order_sell(sym, size)
        DB.register_new_trade(sym,dir,0, created=datetime.now())

def close_half_cycle(sym, dir, size, strategy_type):
    # check if any trade remains and close it.
    # log an sms
    if strategy_type == "minus_step_one_buy":
        if dir == 0:
            mq.order_sell(sym, size)
        elif dir == 1:
            mq.order_buy(sym, size)
    # might want to include trade details like
    # # drawdown reached. 
    # # Data analysis about possible spring ups above close, etc
    # would possibly make use of closefirststep, updateposition etc if we incorporate reaching for springups
    DB.register_closing_position(sym, dir)


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