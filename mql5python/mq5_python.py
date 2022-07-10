from time import time
import MetaTrader5 as mt5
import pandas as pd
from db import db as DB
import strategies as ST


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

def calculate_lot(strategy_name):
    """"""
    return 2          

def order_buy(symbol, strategy_name):
    lot = calculate_lot(strategy_name)
    magic_number = ST.magic_numbers[strategy_name]

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "order_buy: not found, can not call order_check()")
        mt5.shutdown()
        quit()
    
    if not symbol_info.visible:
        print(symbol, "order_buy: is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("order_buy: symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
    
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20
    """
    !caution: actually removed stop loss and take profit
        "sl": price - 100 * point,
        "tp": price + 100 * point,
    """
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "price": price,
        "deviation": deviation,
        "magic": magic_number,
        "comment": "python buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    print("order_buy: 1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_buy: 2. order_send failed, retcode={}".format(result.retcode))
        return None
        # request the result as a dictionary and display it element by element
    # TODO might want to email or text responsible person about the order results.
    return price

def order_sell(symbol, strategy_name):
    lot = calculate_lot(strategy_name)
    magic_number = ST.magic_numbers[strategy_name]

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "order_sell: not found, can not call order_check()")
        mt5.shutdown()
        quit()
    
    if not symbol_info.visible:
        print(symbol, "order_sell: is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("order_sell: symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
    
    # point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
    """
    !caution: actually removed stop loss and take profit
        "sl": price - 100 * point,
        "tp": price + 100 * point,
    """
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL_LIMIT,
        "price": price,
        "deviation": deviation,
        "magic": magic_number,
        "comment": "python sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    print("order_to_sell: 1. order_sell(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result != None: 
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("order_sell: 2. order_sell failed, retcode={}".format(result.retcode))
            return None
            # request the result as a dictionary and display it element by element
    # TODO might want to email or text responsible person about the order results.
    return price

def close_all(sym, strategy_name):
    check_closed = []
    magic_number = ST.magic_numbers[strategy_name]

    all_positions = mt5.positions_get(symbol=sym)
    if all_positions==None:
        """"""
    elif len(all_positions)>0:
        df=pd.DataFrame(list(all_positions),columns=all_positions[0]._asdict().keys())
        for _, row in df.iterrows():
            if row['magic'] == magic_number:
                if sym == "":
                    sym=row['symbol']
                if row['type'] == 0: #current a short, buy to close.
                    check_closed.append(close(row['type'], row['volume'], magic_number, mt5.ORDER_TYPE_BUY_LIMIT, row['ticket'], mt5.symbol_info_tick(sym).ask))
                    # check_closed.append(close(sym, row['ticket']))
                if row['type'] == 1:  #long, sell to close
                    check_closed.append(close(sym, row['volume'], magic_number, mt5.ORDER_TYPE_SELL_LIMIT, row['ticket'], mt5.symbol_info_tick(sym).bid))
                    # check_closed.append(close(sym, row['ticket']))
    

def close(sym, volume,magic_wanted, order_type, ticket, price):
    """"""
    close_request={
        "action": mt5.TRADE_ACTION_CLOSE_BY,
        "symbol": sym,
        "volume": volume,
        "type": order_type,
        "position": ticket,
        "price": price,
        "deviation": 20,
        "magic": magic_wanted,
        "comment": "python close",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # print(close_request)
    close_order=  mt5.Close(sym, ticket)
    print(close_order)
    return close_order

def shutdown():
    mt5.shutdown()