from time import time
from types import NoneType
import MetaTrader5 as mt5
import pandas as pd
from db import db as DB
import strategies as ST
import util as UT


path = "C:/Program Files/MetaTrader 5/terminal64.exe"

def account_login(login,password, server):
    if mt5.login(login,password,server):
        print("logged in succesffully")
    else: 
        print("login failed, error code: {}".format(mt5.last_error()))

def initialize(login, server, password, path=path):
    
    if not mt5.initialize(path):
        print("Initialization failed, error code {}", mt5.last_error())
    else:
        account_login(login, password, server)

def calculate_lot():
    """"""
    account_info=mt5.account_info()
    if account_info!=None:   
        balance = account_info._asdict()['balance']
        if balance > 2000:
            print("good balance {}", balance)
            return round(balance / 20000, 2)
        else:
            UT.critical_error("too little balance {}".format(balance))
            return None
    else:
        print("account info is empty")
        return None

def shutdown():
    mt5.shutdown()


def positions_get(symbol=None):
    if(symbol is None):
        res = mt5.positions_get()
    else:
        res = mt5.positions_get(symbol=symbol)
    if(res is not None and res != ()):
        df = pd.DataFrame(list(res),columns=res[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    return pd.DataFrame()

def close_position(deal_id, strategy_name):
    open_positions = positions_get()
    open_positions = open_positions[open_positions['ticket'] == deal_id]
    order_type  = open_positions["type"][0]
    symbol = open_positions['symbol'][0]
    volume = open_positions['volume'][0]

    if(order_type == mt5.ORDER_TYPE_BUY):
        order_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    else:
        order_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
	
    close_request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_type,
        "position": deal_id,
        "price": price,
        "magic": ST.magic_numbers[strategy_name],
        "comment": "Close trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(close_request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to close order :(")
        return False
    else:
        print ("Order successfully closed!")
        return True

def close_positons_by_symbol(symbol, strategy_name):
    open_positions = positions_get(symbol)
    if len(open_positions) > 0:
        open_positions['ticket'].apply(lambda x: close_position(x, strategy_name))


def open_position(pair, order_type, strategy_name):
    size = calculate_lot()
    if size == None:
        print("account too small to maintain margin")
        return None
    symbol_info = mt5.symbol_info(pair)
    if symbol_info is None:
        print(pair, "not found")
        return

    if not symbol_info.visible:
        print(pair, "is not visible, trying to switch on")
        if not mt5.symbol_select(pair, True):
            print("symbol_select({}}) failed, exit",pair)
            return
    print(pair, "found!")
    
    if(order_type == "BUY"):
        order = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(pair).ask
            
    if(order_type == "SELL"):
        order = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(pair).bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": pair,
        "volume": float(size),
        "type": order,
        "price": price,
        "magic": ST.magic_numbers[strategy_name],
        "comment": "",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to send order :(")
        return False
    else:
        print ("Order successfully placed!")
        return True

def order_sell(symbol, strategy_name):
    return open_position(symbol, "SELL", strategy_name)

def order_buy(symbol, strategy_name):
    return open_position(symbol, "BUY", strategy_name)