import base64
import io
import pathlib
from pathlib import Path

from PIL import Image
from PIL.Image import Image as PILImage

from pastel.models import BaseImage


def load_image(file_path: str | Path) -> PILImage:
    with open(file_path, "rb") as f:
        image = Image.open(io.BytesIO(f.read())).convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255))
    return Image.alpha_composite(background, image).convert("RGB")


def encode_base64(image: PILImage) -> str:
    """
    Converts a PIL Image to a base64-encoded string for API usage.
    """
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")  # OpenAI supports PNG or JPEG
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")


def load_images_from_directory(image_dir: str | Path) -> dict[str, BaseImage]:
    return {
        image.name: BaseImage(image_path=image, image=load_image(image))
        for image in pathlib.Path(image_dir).glob("*.png")
    }
