import pixeltable as pxt
from pixeltable.io import import_huggingface_dataset
from datasets import load_dataset


def import_screenshots():
    dataset = load_dataset("XeIaso/switch-screenshots")
    screenshots = pxt.create_table("screenshots", source=dataset)
    screenshots.add_embedding_index(
        "image",
        embedding=clip.using(model_id="openai/clip-vit-large-patch14"),
    )
    return screenshots


def load_screenshots():
    try:
        return pxt.get_table("screenshots")
    except:
        return import_screenshots()


def search(screenshots: pxt.Table, query: str) -> pxt.ResultSet:
    sim = screenshots.image.similarity(query)
    results = (
        screenshots.order_by(sim, asc=False)
        .select(similarity=sim, image=screenshots.image)
        .limit(6)
    )
    return results.collect()
