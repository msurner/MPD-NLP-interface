from flask import Flask
app = Flask(__name__)

@app.route("/<username>")
def hello(username):
    print("REQUEST: " + username)
    return "Hello " + username
