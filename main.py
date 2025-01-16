from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/current_compet_info")
def current_competitors_info():
    df = pd.read_csv('competitors.csv')
    return render_template("current_info.html", data=df.to_dict())


@app.route("/letter_compet/<letter>")
def letter_competitor(letter):
    df = pd.read_csv('competitors.csv')
    df = df.where(df['name'].str.startswith(letter)).dropna()
    df = pd.DataFrame(df)
    return render_template("letter_compet.html", data=df.to_dict())