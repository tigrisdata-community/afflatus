import base64
import boto3
import os
import pixeltable as pxt
import PIL.Image
from botocore.client import Config
from datasets import load_dataset
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_from_directory, redirect
from flask_htmx import HTMX
from openai import OpenAI
from typing import cast
from urllib.parse import urlparse
from uuid_extensions import uuid7

load_dotenv()
oai = OpenAI()


@pxt.udf
def gen_uuid() -> str:
    return str(uuid7())


def import_screenshots():
    dataset = load_dataset("XeIaso/switch-screenshots")
    screenshots = pxt.create_table("screenshots", source=dataset)
    screenshots.add_embedding_index(
        "image",
        embedding=clip.using(model_id="openai/clip-vit-large-patch14"),
    )
    screenshots.add_computed_column(uuid=gen_uuid())
    return screenshots


try:
    screenshots = pxt.get_table("screenshots")
except:
    screenshots = import_screenshots()
assert screenshots is not None
screenshots = cast(pxt.Table, screenshots)


@pxt.query
def get_image(image_id: str) -> Image.Image:
    return (
        screenshots.where(screenshots.uuid == image_id)
        .select(screenshots.image)
        .limit(1)
    )


def encode_image(file_path):
    with open(file_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    return base64_image


# @pxt.udf
# def image_edit(prompt: str, input: PIL.Image.Image) -> PIL.Image.Image:
#     pass


generated_images = pxt.create_table(
    "generated_images",
    {
        "input_image_id": pxt.String,
        "prompt": pxt.String,
    },
    if_exists="ignore",
)
assert generated_images is not None, (
    "creating the table did not result in creating the table"
)
generated_images.add_computed_column(uuid=gen_uuid())
generated_images.add_computed_column(
    input_image=get_image(generated_images.input_image_id)
)
# generated_images.add_computed_column(
#     gen_image=image_generations(generated_images.prompt, model="gpt-image-1")
# )


def perform_search(screenshots: pxt.Table, query: str) -> pxt.ResultSet:
    sim = screenshots.image.similarity(query)
    results = (
        screenshots.order_by(sim, asc=False)
        .select(
            uuid=screenshots.uuid,
            url=screenshots.image.fileurl,
        )
        # .limit(6)
        .limit(1)
    )
    return results.collect()


app = Flask(__name__)
htmx = HTMX(app)
tigris = boto3.client(
    "s3",
    endpoint_url="https://t3.storage.dev",
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "virtual"},
    ),
)


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

    hits = perform_search(screenshots, query)
    results = []

    for hit in hits:
        print(hit)
        uuid = hit["uuid"]
        url = hit["url"]

        # Parse S3 URL to extract bucket and key
        parsed_url = urlparse(url)
        bucket = parsed_url.netloc
        key = parsed_url.path[1:]
        print(bucket, key)

        presigned_url = tigris.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=3600,
        )

        results.append(
            {
                "id": uuid,
                "url": presigned_url,
            }
        )

    return render_template(
        "partials/api/search.html",
        query=query,
        results=results,
    )
