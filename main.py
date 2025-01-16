from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/current_compet_info")
def current_competitors_info():
    return


@app.route("/letter_compet/{letter}")
def letter_competitor():
    return