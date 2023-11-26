from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world!"

@app.route("/hamza")
def hello_hamza():
    return "hello hamza!"

@app.route("/details")
def details():
    return "name : hamza\n       age : 18\n             IDE : VScode"

app.run(debug=True)