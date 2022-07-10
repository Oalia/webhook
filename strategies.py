

chill_a_little ="just_chill"
minus_step = "minus_step_one_buy"

BUY = "buy"
SELL = "sell"
magic_numbers = {chill_a_little: 1, minus_step: 2}

def login_details(strategy):
    if strategy == chill_a_little:
        return {"name": 50902855, "key": "eXG8GpQ4", "server": "ICMarketsSC-Demo"}
    if strategy == minus_step:
        return {"name": 50901624, "key": "9qeEYbCF", "server": "ICMarketsSC-Demo"}

