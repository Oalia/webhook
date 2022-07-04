from time import time
import MetaTrader5 as mt5
import pandas as pd

name = 50901624
key = "9qeEYbCF"
serv = "ICMarketsSC-Demo"
path = "C:/Program Files/MetaTrader 5/terminal64.exe"
lot = 0.02
#  path,                     // path to the MetaTrader 5 terminal EXE file
#    login=LOGIN,              // account number
#    password="PASSWORD",      // password
#    server="SERVER",          // server name as it is specified in the terminal
#    timeout=TIMEOUT,          // timeout
#    portable=False   

def account_login(login = name,password=key, server= serv,):
    if mt5.login(login,password,server):
        print("logged in succesffully")
    else: 
        print("login failed, error code: {}".format(mt5.last_error()))

def initialize(login = name, server=serv, password=key, path=path):
    
    if not mt5.initialize(path):
        print("Initialization failed, error code {}", mt5.last_error())
    else:
        account_login(login, password, server)
    
def order_buy(symbol = "USDJPY", lot = 0.01, magic_id=0000):
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
        "magic": magic_id,
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

def order_sell(symbol = "USDJPY", lot = 0.01, magic_id=0000):
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
        "magic": magic_id,
        "comment": "python sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    print("order_sell: 1. order_sell(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_sell: 2. order_sell failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
    # TODO might want to email or text responsible person about the order results.
    return result

def close_all(sym):
    check_closed = []

    all_positions = mt5.positions_get(symbol=sym)
    if all_positions==None:
        """"""
    elif len(all_positions)>0:
        df=pd.DataFrame(list(all_positions),columns=all_positions[0]._asdict().keys())
        for _, row in df.iterrows():
            if row['type'] == 0: #current a short, buy to close.
                check_closed.append(close(sym, row['volume'], row['magic'], mt5.ORDER_TYPE_BUY_LIMIT, row['ticket'], mt5.symbol_info_tick(sym).ask))

            if row['type'] == 1:  #long, sell to close
                check_closed.append(close(sym, row['volume'], row['magic'], mt5.ORDER_TYPE_SELL_LIMIT, row['ticket'], mt5.symbol_info_tick(sym).bid))

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
    return mt5.order_send(close_request)

def order_close_by_magic(sym, magic_wanted):
    all_positions = mt5.positions_get(symbol=sym)
    if all_positions==None:
        """"""
    elif len(all_positions)>0:
        df=pd.DataFrame(list(all_positions),columns=all_positions[0]._asdict().keys())
        for _, row in df.iterrows():
            if row['magic'] == magic_wanted:
                if row['type'] == 0:
                    close(sym, row['volume'], magic_wanted, mt5.ORDER_TYPE_SELL_LIMIT,row['ticket'], mt5.symbol_info_tick(sym).bid)
                else:
                    close(sym, row['volume'], magic_wanted, mt5.ORDER_TYPE_BUY_LIMIT,row['ticket'], mt5.symbol_info_tick(sym).ask)


def shutdown():
    mt5.shutdown()

# def order_buy_close(result, symbol, lot = 0.01):
#     # create a close request
#     position_id=result.order
#     price=mt5.symbol_info_tick(symbol).bid
#     deviation=20
#     request={
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_SELL,
#         "position": position_id,
#         "price": price,
#         "deviation": deviation,
#         "magic": 234000,
#         "comment": "python script close",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_RETURN,
#     }
#     # send a trading request
#     result=mt5.order_send(request)
#     # check the execution result
#     print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation))
#    
#     while(result.retcode != mt5.TRADE_RETCODE_DONE):
#         order_buy_close(result, symbol, lot)
#         print("4. buy_selling_close order_send failed, retcode={}".format(result.retcode))
#         print("   result",result)
#     print("4. position #{} closed, {}".format(position_id,result))
#     return order_sell(symbol, lot)
#    
# def order_sell_close(result, symbol, lot = 0.01):
#     # create a close request
#     position_id=result.order
#     price=mt5.symbol_info_tick(symbol).ask
#     deviation=20
#     request={
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_BUY,
#         "position": position_id,
#         "price": price,
#         "deviation": deviation,
#         "magic": 234000,
#         "comment": "python script close",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_RETURN,
#     }
#     # send a trading request
#     result=mt5.order_send(request)
#     # check the execution result
#     print("3. sell buying close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
# 
#     while(result.retcode != mt5.TRADE_RETCODE_DONE):
#         order_sell_close(result, symbol, lot)
#         print("4. sell_buying_close order_send failed, retcode={}".format(result.retcode))
#         print("   result",result)
#     print("4. position #{} closed, {}".format(position_id,result))
#     return order_buy(symbol, lot)
# 
# def symbols_total():
#     # get the number of financial instruments
#     symbols=mt5.symbols_total()
#     if symbols>0:
#         print("Total symbols =",symbols)
#     else:
#         print("symbols not found")