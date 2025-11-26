import os
from flask import Flask, render_template, send_from_directory
from flask_htmx import HTMX


app = Flask(__name__)
htmx = HTMX(app)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/healthz")
def healthz():
    return "OK"


@app.route("/")
def index():
    if htmx:
        return render_template("partials/index_content.html")
    return render_template("pages/index.html")
