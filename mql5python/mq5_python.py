import MetaTrader5 as mt5

name = "your number"
key = "your key"
serv = "Pepperstone-MT5-Live01"
path = r"C:\Program Files\MetaTrader 5 B\terminal64.exe"
# symbol = "EURUSD"
lot = 0.02


def initialize(login = name, server=serv, password=key, path = path):
    if not mt5.initialize(login, server, password, path):
        print("initialize() failed, error code =", mt5.last_error())
        initialize(login, server, password, path)
    
def order_buy(symbol = "USDJPY", lot = 0.01):
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
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    print("order_buy: 1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_buy: 2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
    # TODO might want to email or text responsible person about the order results.
    return result


def order_sell(symbol = "USDJPY", lot = 0.01):
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
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
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