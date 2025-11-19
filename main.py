from flask import Flask, render_template
from flask_htmx import HTMX


app = Flask(__name__)
htmx = HTMX(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
