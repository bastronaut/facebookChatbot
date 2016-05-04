from flask import Flask, request
app = Flask(__name__)

token = 'test'
# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route('/fbchatbot/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == token:
        print requests.args
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

if __name__ == "__main__":
    app.run(debug=True)
