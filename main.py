from flask import Flask, render_template
from flask_htmx import HTMX


app = Flask(__name__)
htmx = HTMX(app)


@app.route("/healthz")
def healthz():
    return "OK"


@app.route("/")
def index():
    if htmx:
        return render_template("partials/index_content.html")
    return render_template("pages/index.html")
