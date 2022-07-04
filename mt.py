import MetaTrader5 as mt5

name = "50901624"
key = "9qeEYbCF"
serv = "ICMarketsSC-Demo"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
     
mt5.initialize(name, serv, key, path)



# request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_SELL,
#         "sl": price - 0.002,
#         "tp": price + 0.005,
#         "deviation": deviation,
#         "magic": 202003,
#         "comment": "InUpBot MrEurUsd",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_IOC
#     }
# print('Se ejecutó una compra por 0.01')
# mt5.order_send(request)
        
# request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_BUY,
#         "sl": price + 0.002,
#         "tp": price - 0.005,
#         "deviation": deviation,
#         "magic": 202003,
#         "comment": "InUpBot Lancero",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_IOC
#     }