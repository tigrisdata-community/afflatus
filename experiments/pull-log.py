import pixeltable as pxt
from pixeltable.functions import openai, yolox
from pixeltable.iterators.video import FrameIterator

pxt.drop_table("content", force=True)
videos = pxt.create_table(
    "content",
    schema={
        "video": pxt.Video,
        "title": pxt.String,
    },
    if_exists="ignore",
)

videos.insert(
    [
        {
            "video": "./var/pt-solo-floor-50-r30.mp4",
            "title": "Pilgrim's Traverse Stone 50 (Solo as White Mage)",
        },
        # {
        #     "video": "./var/botw-hateno-fight.mp4",
        #     "title": "Breath of the Wild - Random Hateno fight",
        # },
    ]
)

# videos = pxt.get_table("content")

# Automatic frame extraction
frames = pxt.create_view(
    "frames", videos, iterator=FrameIterator.create(video=videos.video, fps=1)
)

# Define what you want computed - runs automatically
frames.add_computed_column(objects=yolox.yolox(frames.frame, model_id="yolox_s"))

# frames.add_computed_column(
#     description=openai.vision(
#         frames.frame,
#         prompt="Describe what's happening in this frame",
#         model="gpt-4.1-nano",
#     )
# )
