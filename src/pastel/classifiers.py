from typing import Literal, cast

from pydantic_ai import Agent

from pastel.config import OPENAI_MODEL
from pastel.models import BaseImage, InsightPlots

ImageType = Literal["pricing", "severity", "frequency", "cuts"]

classifier = Agent(
    model=OPENAI_MODEL,
    system_prompt="""
        Classify this insurance visualization image into exactly one of these four categories:

        1. pricing - A chart showing pricing changes over time, often showing premium trends
        2. severity - A chart showing claim severity metrics, often showing ratios of large claims to total claims
        3. frequency - A chart showing claim frequency over time, measuring how often claims are filed
        4. cuts - A chart showing business segment analysis, breaking down metrics by categories/segments

        Return ONLY the category name as a single word: "pricing", "severity", "frequency", or "cuts".
        Do not include any other text, explanation, or punctuation in your response.
        """,
)


async def classify_insurance_image(image_obj: BaseImage) -> ImageType:
    """
    Classify an insurance visualization image into one of the four expected types:
    - pricing: Time series of pricing changes
    - severity: Claim severity metrics
    - frequency: Claim frequency metrics
    - cuts: Business segment analysis

    Args:
        image_obj: BaseImage object containing the image to classify

    Returns:
        Classification as one of the four expected image types
    """

    # Use the image object directly with no encoding logic in this function
    result = classifier.run_sync(
        ["Classify this insurance visualization image:", image_obj.binary_content]
    )

    # Process the classification result
    classification = result.data.strip().lower()
    if classification not in ["pricing", "severity", "frequency", "cuts"]:
        # Default to the most likely category if we get an unexpected response
        # TODO Make this a match/case statement
        if "price" in classification or "premium" in classification:
            return "pricing"
        elif "sever" in classification:
            return "severity"
        elif "freq" in classification:
            return "frequency"
        else:
            return "cuts"

    return cast(ImageType, classification)


async def classify_images(images: InsightPlots) -> dict[ImageType, BaseImage]:
    """
    Classify a collection of insurance images into the four expected types.

    Args:
        images: List of BaseImage objects to classify

    Returns:
        Dictionary mapping image types to their corresponding BaseImage objects
    """
    image_dict = {}

    for img in images:
        category = await classify_insurance_image(img)
        image_dict[category] = img

    return image_dict
