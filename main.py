import os
from flask import Flask, render_template, send_from_directory, redirect
from flask_htmx import HTMX
from time import sleep


app = Flask(__name__)
htmx = HTMX(app)


def simple_page(name):
    if htmx:
        return render_template(f"partials/{name}.html")
    return render_template(f"pages/{name}.html")


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
    return simple_page("index")


@app.route("/search")
def search():
    return simple_page("search")


@app.route("/api/search", methods=["POST"])
def api_search():
    if not htmx:
        return redirect("/search")

    # Search pixeltable
    sleep(2)

    return render_template(
        "partials/api/search.html",
        results=[
            {
                "id": "image1",
                "url": "https://files.xeiaso.net/hero/puppy-bunky.jpg",
            },
            {
                "id": "image2",
                "url": "https://files.xeiaso.net/hero/dgx-spark.jpg",
            },
            {
                "id": "image3",
                "url": "https://files.xeiaso.net/hero/around-the-bend.jpg",
            },
        ],
    )
