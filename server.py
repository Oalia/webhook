from flask import Flask, request, abort
import json
app = Flask (__name__)

@app.route('/',)
def begin():
    return "hi"

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         print("hello webhook")

#         webhook_msg = json.loads(request.data)
#         ticker = webhook_msg['ticker']
#         time = webhook_msg['time']
#         volume = webhook_msg['bar']['volume']
        
#         print(ticker, time, volume)
#         return 'success', 200
#     else:
#         abort(400)

if __name__ == '__main__':
    app.run(debug=True)