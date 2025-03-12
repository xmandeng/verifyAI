import base64
import io
import pathlib
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as PILImage

from pastel.models import BaseImage, InsightModel, InsightPlots


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


def create_consolidated_image(
    lrs_data: pd.DataFrame, images: InsightPlots, insight: InsightModel
) -> BaseImage:

    # Define the output path for the consolidated image
    output_path = Path(f"../data/{insight.name.replace('/', '-')}_consolidated_image.png")

    # Create a blank image with white background
    width, height = 1200, 2000  # Increase height to accommodate larger images
    consolidated_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(consolidated_image)

    # Load a font
    font = ImageFont.load_default()

    # Draw LRS Data table with bounding box
    x_offset, y_offset = 50, 50
    table_width = 500
    table_height = (len(lrs_data) + 2) * 20
    draw.rectangle(
        [x_offset - 10, y_offset - 10, x_offset + table_width, y_offset + table_height],  # type: ignore
        outline="black",
    )
    draw.text((x_offset, y_offset), "LRS Data", font=font, fill="black")
    y_offset += 20
    for col in lrs_data.columns:
        draw.text((x_offset, y_offset), col, font=font, fill="black")
        x_offset += 100
    y_offset += 20
    x_offset = 50
    for index, row in lrs_data.iterrows():
        for col in lrs_data.columns:
            draw.text((x_offset, y_offset), str(row[col]), font=font, fill="black")
            x_offset += 100
        y_offset += 20
        x_offset = 50

    # Draw images with captions and bounding boxes in a single column
    x_offset = 600
    y_offset = 50

    for plot in images.plots:
        image_path = Path(f"../data/{insight.name.replace('/', '-')}/{plot}")
        img = Image.open(image_path)
        img = img.convert("RGBA")  # Convert image to RGBA to handle transparency
        # Create a white background image
        white_bg = Image.new("RGBA", img.size, "white")
        # Composite the image onto the white background
        img = Image.alpha_composite(white_bg, img).convert("RGB")
        img.thumbnail((500, 500))  # Increase thumbnail size for better legibility
        img_width, img_height = img.size

        draw.rectangle(
            [x_offset - 10, y_offset - 10, x_offset + img_width + 10, y_offset + img_height + 40],  # type: ignore
            outline="black",
        )
        draw.text((x_offset, y_offset), plot, font=font, fill="black")
        y_offset += 20
        consolidated_image.paste(img, (x_offset, y_offset))
        y_offset += img_height + 40  # Adjust spacing for larger images

    # Save the consolidated image
    consolidated_image.save(output_path)

    # Return a BaseImage object
    return BaseImage(image_path=output_path, image=consolidated_image)
