import pixeltable as pxt
import PIL.Image
from pixeltable.io import import_huggingface_dataset
from pixeltable.functions.openai import image_generations
from datasets import load_dataset
from uuid_extensions import uuid7


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


def load_screenshots():
    try:
        return pxt.get_table("screenshots")
    except:
        return import_screenshots()


@pxt.query
def filtered_search(query: str, category: str):
    sim = docs.content.similarity(query)

    return (
        docs.where(docs.metadata["category"] == category)
        .order_by(sim, asc=False)
        .select(docs.content, score=sim)
        .limit(5)
    )


@pxt.query
def get_image(image_id: str) -> PIL.Image.Image:
    return (
        screenshots.where(screenshots.uuid == image_id)
        .select(screenshots.image)
        .limit(1)
    )


def load_generated_images(screenshots: pxt.Table) -> pxt.Table:
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
        gen_image=image_generations(generated_images.prompt, model="gpt-image-1")
    )
