from db  import db as DB
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
    ""
def enter_new_position(sym, dir, size):
    ""
    # enter first position, get it's db id, update its depth when other positions get filled
    depth = 0
    entry_price = 0
    hedge(sym, dir)
    DB.register_new_trade(sym, dir, depth, entry_price)

def close_positions(sym, dir, size):
    # check if any trade remains and close it.
    # log an sms
    ""
    DB.register_closing_position(sym, status = "closed")

def close_first_step(dir, sym, depth):
    ""

def close_second_step(dir, sym, depth):
    ""

def shift_stoploss(dir, sym, step, depth, entry_price):
    """
        # calculations for shifting stop loss
    """

def update_position(dir, sym, step, depth, entry_price):
    if step == 0:
        close_first_step(dir, sym, depth)
    if step == 1:
        close_second_step(dir, sym, depth)
    else:
        shift_stoploss(dir, sym, step, depth, entry_price)
        ""
    DB.update_step(sym)