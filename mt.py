import pandas as pd
import numpy as np
import datetime
from datetime import datetime
from datetime import date
import MetaTrader5 as mt5
import time

name = "your number"
key = "your key"
serv = "Pepperstone-MT5-Live01"
path = r"C:\Program Files\MetaTrader 5 B\terminal64.exe"
symbol = "EURUSD"
lot = 0.02 

# Get the Data
mt5.initialize( login = name, server = serv, password = key, path = path)
symbol_info=mt5.symbol_info("EURUSD")
        

price = mt5.symbol_info_tick(symbol).ask
deviation = 20


request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "sl": price - 0.002,
        "tp": price + 0.005,
        "deviation": deviation,
        "magic": 202003,
        "comment": "InUpBot MrEurUsd",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
print('Se ejecutó una compra por 0.01')
mt5.order_send(request)
        
        
request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "sl": price + 0.002,
        "tp": price - 0.005,
        "deviation": deviation,
        "magic": 202003,
        "comment": "InUpBot Lancero",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

print('Se ejecutó una venta por 0.01')
mt5.order_send(request)


