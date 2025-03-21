import base64
import io
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Literal, Optional

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field, SkipValidation, field_validator
from pydantic_ai import BinaryContent

ImageType = Literal["pricing", "severity", "frequency", "cuts"]


class InputModel(BaseModel):
    name: str = Field(description="Program name")
    insight: str = Field(description="Insight text")
    line_of_business: str = Field(description="Line of business for this program")


class AssertionModel(InputModel):
    conclusion: str = Field(
        description="The main driving point or central assertion within an insight that represents the primary takeaway or judgment being made"
    )


class Evidence(BaseModel):
    evidence: Optional[list[str]] = Field(
        description="A collection of supporting facts or observations that substantiate the assertion"
    )


class InsightModel(AssertionModel, Evidence):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )


class Assessment(InsightModel):
    decision: bool = Field(
        description="Whether the assertion is supported by evidence and logically valid"
    )
    reason: list[str] = Field(
        description="The specific justifications explaining why the assertion was determined to be valid or invalid"
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    def __bool__(self):
        return self.decision


class PremiseValidation(BaseModel):
    claim: str = Field(description="The specific claim being validated")
    status: Literal["True", "Partially True", "False", "NotFound"] = Field(
        description="Validation status of the claim"
    )
    confidence: Literal["High", "Medium", "Low"] = Field(
        description="Confidence level in the validation assessment"
    )
    reasoning: str = Field(description="Explanation of validation logic")


class InsightValidation(BaseModel):
    overall_valid: bool = Field(description="Whether the entire insight is considered valid")
    reasoning: str = Field(description="Summary explanation of validation results")


class GrammarValidation(BaseModel):
    errors: list[str] = Field(description="Grammar errors in the insight")


class BaseImage(BaseModel):
    image_path: Path = Field(..., description="Path to the image file")
    image: Annotated[Image.Image, SkipValidation] = Field(..., description="The image object")
    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
        extra="forbid",
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
    )

    @field_validator("image_path", mode="before")
    @classmethod
    def validate_image_path(cls, path):
        if not os.path.exists(path):
            raise ValueError(f"File not found: {path}")
        return path

    @field_validator("image_path", mode="after")
    @classmethod
    def convert_str_to_path(cls, path):
        if isinstance(path, str):
            return Path(path)
        return path

    @property
    def encoded(self) -> str:
        """
        Converts a PIL Image to a base64-encoded string for API usage.
        """
        buffer = io.BytesIO()
        self.image.save(buffer, format="JPEG")  # OpenAI supports PNG or JPEG
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode("utf-8")

    @property
    def binary_content(self) -> BinaryContent:
        """
        Converts the image to a BinaryContent object for use with LLM APIs.

        Args:
            description: Optional description of the image content

        Returns:
            BinaryContent object ready for use with PydanticAI
        """
        buffer = io.BytesIO()
        self.image.save(buffer, format="JPEG")
        buffer.seek(0)

        return BinaryContent(
            data=buffer.getvalue(),
            media_type="image/jpeg",
        )


class InsightPlots(BaseModel):
    plots: dict[str, BaseImage] = Field(
        ..., description="Dictionary of plot names and corresponding base64-encoded images"
    )
    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        arbitrary_types_allowed=True,
    )

    def __iter__(self):
        return iter(self.plots.values())

    def count(self) -> int:
        return len(self.plots)


class BaseDocument(BaseModel):
    """Represents a PDF document as a binary content object."""

    binary_content: BinaryContent
    filename: str


@dataclass
class EvaluationInput:
    insight: InsightModel
    premises: list[PremiseValidation]
    grammar: GrammarValidation
