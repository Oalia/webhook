from flask import Flask, request, abort
import json
app = Flask (__name__)

@app.route('/',)
def begin():
    return "hi"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("hello webhook")

        webhook_msg = json.loads(request.data)
        # ticker = webhook_msg['ticker']
        # time = webhook_msg['time']
        # volume = webhook_msg['bar']['volume']
        
        print(webhook_msg)
        return 'success', 200
    else:
        abort(400)

@app.route('/github', method = ['POST'])
def api_gh_message():
    if request.headers['Content-Type']== 'application/json':
        return json.dumps(request.json)

if __name__ == '__main__':
    app.run(debug=True)