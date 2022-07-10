from time import time
import MetaTrader5 as mt5
import pandas as pd

serv = "ICMarketsSC-Demo"
path = "C:/Program Files/MetaTrader 5/terminal64.exe"
lot = 0.02

# name = 50901624
# key = "9qeEYbCF"

name = 50902855
key = "eXG8GpQ4"
#  path,                     // path to the MetaTrader 5 terminal EXE file
#    login=LOGIN,              // account number
#    password="PASSWORD",      // password
#    server="SERVER",          // server name as it is specified in the terminal
#    timeout=TIMEOUT,          // timeout
#    portable=False


def account_login(
    login=name,
    password=key,
    server=serv,
):
    if mt5.login(login, password, server):
        print("logged in succesffully")
    else:
        print("login failed, error code: {}".format(mt5.last_error()))


def initialize(login=name, server=serv, password=key, path=path):

    if not mt5.initialize(path):
        print("Initialization failed, error code {}", mt5.last_error())
    else:
        account_login(login, password, server)


def order_buy(symbol="USDJPY", lot=0.01, magic_id=0000):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "order_buy: not found, can not call order_check()")
        mt5.shutdown()
        quit()

    if not symbol_info.visible:
        print(symbol, "order_buy: is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("order_buy: symbol_select({}}) failed, exit", symbol)
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
    print(
        "order_buy: 1. order_send(): by {} {} lots at {} with deviation={} points"
        .format(symbol, lot, price, deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_buy: 2. order_send failed, retcode={}".format(
            result.retcode))
        return None
        # request the result as a dictionary and display it element by element
    # TODO might want to email or text responsible person about the order results.
    return price


def order_sell(symbol="USDJPY", lot=0.01, magic_id=0000):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "order_sell: not found, can not call order_check()")
        mt5.shutdown()
        quit()

    if not symbol_info.visible:
        print(symbol, "order_sell: is not visible, trying to switch on")
        if not mt5.symbol_select(symbol, True):
            print("order_sell: symbol_select({}}) failed, exit", symbol)
            mt5.shutdown()
            quit()

    # point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 20
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
    print(
        "order_sell: 1. order_sell(): by {} {} lots at {} with deviation={} points"
        .format(symbol, lot, price, deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_sell: 2. order_sell failed, retcode={}".format(
            result.retcode))
        return None
        # request the result as a dictionary and display it element by element
    # TODO might want to email or text responsible person about the order results.
    return price



def order_close_by_magic(sym, magic_wanted):
    close_positons_by_symbol_or_magic(magic_wanted)
    # all_positions = mt5.positions_get(symbol=sym)
    # if all_positions == None:
    #     print("No symbol found close magic")
    # elif len(all_positions) > 0:
    #     df = pd.DataFrame(list(all_positions),
    #                       columns=all_positions[0]._asdict().keys())
    #     for _, row in df.iterrows():
    #         if row['magic'] == magic_wanted:
    #             # if row['type'] == 0:
    #             close(sym, row['ticket'])
    #             # row['volume'], magic_wanted, mt5.ORDER_TYPE_SELL_LIMIT,row['ticket'], mt5.symbol_info_tick(sym).bid)
    #             # else:
    #             #     close(sym, row['volume'], magic_wanted, mt5.ORDER_TYPE_BUY_LIMIT,row['ticket'], mt5.symbol_info_tick(sym).ask)


def shutdown():
    mt5.shutdown()


def positions_get(symbol=None, magic=None):
    """source: https://www.conorjohanlon.com/close-a-trade-with-mt5-using-python/"""
    if (symbol is None and magic is None):
        res = mt5.positions_get()
    else:
        if (symbol is not None):
            res = mt5.positions_get(symbol=symbol)
        elif (magic is not None):
            res = mt5.positions_get(magic=magic)

    if (res is not None and res != ()):
        df = pd.DataFrame(list(res), columns=res[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    return pd.DataFrame()


def close_position(deal_id):
    """source: https://www.conorjohanlon.com/close-a-trade-with-mt5-using-python/"""
    open_positions = positions_get()
    open_positions = open_positions[open_positions['ticket'] == deal_id]
    order_type = open_positions["type"].iloc[0]
    symbol = open_positions['symbol'].iloc[0]
    volume = open_positions['volume'].iloc[0]

    if (order_type == mt5.ORDER_TYPE_BUY):
        order_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    else:
        order_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask

    close_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_type,
        "position": deal_id,
        "price": price,
        "magic": 234000,
        "comment": "Close trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(close_request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to close order :(")
    else:
        print("Order successfully closed!")


def close_positons_by_symbol_or_magic(symbol=None, magic=None):
    """source: https://www.conorjohanlon.com/close-a-trade-with-mt5-using-python/"""
    if symbol is None and magic is not None:
        open_positions = positions_get(magic =magic)
    elif symbol is not None and magic is None:
        open_positions = positions_get(symbol=symbol)
    open_positions['ticket'].apply(lambda x: close_position(x))
