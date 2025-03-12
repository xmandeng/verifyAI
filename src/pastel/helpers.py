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
    """
    Creates a consolidated image containing LRS data and all plots from the program folder.

    Args:
        lrs_data: DataFrame containing LRS data for the program
        images: InsightPlots object containing images for visualization
        insight: InsightModel containing program details

    Returns:
        BaseImage object with the consolidated visualization
    """
    # Define the output path for the consolidated image
    output_path = Path(f"../data/{insight.name.replace('/', '-')}_consolidated_image.png")

    # Create a blank image with white background - use a wider format for better layout
    width, height = 1800, 2000  # Increased width and height for better spacing
    consolidated_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(consolidated_image)

    try:
        # Try to use a nicer font if available
        font_title = ImageFont.truetype("Arial", 16)
        font = ImageFont.truetype("Arial", 12)
    except IOError:
        # Fallback to default font
        font_title = ImageFont.load_default()  # type: ignore
        font = ImageFont.load_default()  # type: ignore

    # Draw title and insight text at the top
    title_y = 20
    draw.text(
        (width // 2 - 200, title_y), f"Program: {insight.name}", font=font_title, fill="black"
    )

    # Section for LRS Data
    lrs_y = title_y + 60  # Increased margin from title
    draw.text((50, lrs_y), "LRS Data", font=font_title, fill="black")

    # Create table frame
    table_width = 550  # Increased table width
    row_height = 35  # Increased row height for better readability
    table_height = (len(lrs_data) + 1) * row_height  # +1 for header

    # Draw table with grid lines
    col_widths = [200, 150, 150]  # Increased width for first column

    # Draw table headers with background
    header_y = lrs_y + 30
    x_pos = 50
    draw.rectangle((x_pos, header_y, x_pos + table_width, header_y + row_height), fill="lightgray")

    # Draw header text
    x_pos = 50
    for i, col in enumerate(lrs_data.columns):
        draw.text((x_pos + 5, header_y + 5), col, font=font, fill="black")
        draw.line(
            (x_pos + col_widths[i], header_y, x_pos + col_widths[i], header_y + table_height),
            fill="black",
        )
        x_pos += col_widths[i]

    # Draw horizontal line after header
    draw.line((50, header_y + row_height, 50 + table_width, header_y + row_height), fill="black")

    # Draw rows
    row_y = header_y + row_height
    for _, row in lrs_data.iterrows():
        x_pos = 50
        for i, col in enumerate(lrs_data.columns):
            cell_text = str(row[col])
            draw.text((x_pos + 5, row_y + 5), cell_text, font=font, fill="black")
            x_pos += col_widths[i]

        row_y += row_height
        draw.line((50, row_y, 50 + table_width, row_y), fill="black")

    # Organize images in a 2x3 grid layout
    plots_per_row = 2
    max_img_width = (width - 150) // plots_per_row  # Added more margin between columns
    max_img_height = 400  # Increased maximum height for each image

    # Calculate starting position for images grid
    grid_start_y = lrs_y + table_height + 100  # Increased spacing after table

    # Process and place each image
    plot_items = list(images.plots.items())
    for idx, (plot_name, img_obj) in enumerate(plot_items):
        # Calculate grid position
        row = idx // plots_per_row  # type: ignore
        col = idx % plots_per_row  # type: ignore

        # Calculate image position
        x_pos = 50 + col * (max_img_width + 75)  # type: ignore
        y_pos = grid_start_y + row * (
            max_img_height + 100
        )  # Increased vertical spacing between image rows

        # Get image and resize while maintaining aspect ratio
        img = img_obj.image.copy()
        img.thumbnail((max_img_width, max_img_height))

        # Get actual size after resizing
        img_width, img_height = img.size

        # Draw border and title for the image
        draw.rectangle(
            (x_pos - 10, y_pos - 30, x_pos + img_width + 10, y_pos + img_height + 10),  # type: ignore
            outline="black",
        )
        draw.text((x_pos, y_pos - 25), plot_name, font=font, fill="black")  # type: ignore

        # Paste the image
        consolidated_image.paste(img, (x_pos, y_pos))  # type: ignore

    # Save the consolidated image
    consolidated_image.save(output_path)

    # Return a BaseImage object
    return BaseImage(image_path=output_path, image=consolidated_image)
