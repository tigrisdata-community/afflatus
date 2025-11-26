import boto3
import os
import pixeltable as pxt
from botocore.client import Config
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_from_directory, redirect
from flask_htmx import HTMX
from openai import OpenAI
from time import sleep
from typing import cast

# App-specific imports
from app.chores import load_screenshots, search


load_dotenv()
app = Flask(__name__)
htmx = HTMX(app)
oai = OpenAI()
tigris3 = boto3.client(
    "s3",
    endpoint_url="https://t3.storage.dev",
    config=Config(s3={"addressing_style": "virtual"}),
)
screenshots = load_screenshots()
assert screenshots is not None
screenshots = cast(pxt.Table, screenshots)


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
        return render_template("partials/index.html")
    return render_template("pages/index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    if not htmx:
        return redirect("/search")

    # Search pixeltable
    query = request.form.get("q", "")

    if query == "":
        return render_template("partials/api/search_empty.html")

    results = search(screenshots, query)

    for result in results:
        print(result)
        image = result["image"]
        print(image.fileurl)

    return render_template(
        "partials/api/search.html",
        query=query,
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
