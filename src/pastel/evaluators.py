import re

from pydantic_ai import Agent
from pydantic_ai.models import KnownModelName

from pastel.models import BaseImage, ImageType, InsightValidation

# from pastel.prompts import EVALUATION_PROMPT

OPENAI_MODEL_MINI: KnownModelName = "openai:gpt-4o-mini"
OPENAI_MODEL: KnownModelName = "openai:gpt-4o"
ANTHROPIC_MODEL: KnownModelName = "anthropic:claude-3-5-sonnet-latest"

# eval_agent = Agent(
#     model=OPENAI_MODEL,
#     deps_type=InsightModel,
#     result_type=InsightValidation,
# )


# @eval_agent.system_prompt
# def build_evidence_prompt(ctx: RunContext[AssertionModel]) -> str:
#     return EVALUATION_PROMPT.format(conclusion=ctx.deps.conclusion)


# async def parse_evidence(claim: InsightModel, insight: str) -> InsightValidation:
#     result = eval_agent.run_sync(insight, deps=claim)
#     return InsightModel(conclusion=claim.conclusion, evidence=result.data.evidence)


async def validate_insight_against_evidence(
    insight_text: str,
    program_name: str,
    line_of_business: str,
    images: dict[ImageType, BaseImage],
    lrs_data: str,
) -> InsightValidation:
    """Validate an entire insight against all available evidence."""

    # Format LRS data for inclusion in prompt
    lrs_summary = lrs_data  # .to_string() if not lrs_data.empty else "No LRS data available"

    # Include image types in the prompt for reference
    image_types_list = ", ".join([re.sub(r"_\d", "", key) for key in images])

    # Create message list starting with the text prompt
    messages = [
        f"""
        Insurance Program: {program_name}
        Line of Business: {line_of_business}

        Insight to validate:
        "{insight_text}"

        Available evidence:

        1. LRS Data:
        {lrs_summary}

        2. Available Images: {image_types_list}

        Validate the insight against this evidence. Break it into individual claims and assess each one.
        """
    ]

    # Add each image to the message list with context
    for image_type, img in images.items():
        messages.append(f"This is the {image_type} visualization:")
        messages.append(str(img.binary_content))

    # Create validator
    validator = Agent(
        model=OPENAI_MODEL,
        system_prompt="""
        You are an expert insurance insight validator. You will analyze an insurance insight statement and validate it against provided evidence.

        For each major claim in the insight, determine if it is:
        - True: Evidence clearly supports the claim
        - Partially True: Evidence supports parts of the claim or shows mixed support
        - False: Evidence clearly contradicts the claim
        - NotFound: No relevant evidence is available to validate the claim

        Also assign a confidence level (High/Medium/Low) to your assessment.

        Return a JSON object with:
        1. A list of claim_validations, each containing:
           - claim: The specific claim text
           - status: "True", "Partially True", "False", or "NotFound"
           - confidence: "High", "Medium", or "Low"
           - source: The evidence source used (image type or "lrs_data")
           - reasoning: Brief explanation of your assessment
        2. overall_valid: Boolean indicating if the entire insight is valid
        3. reasoning: Summary of your validation process

        Important guidelines:
        - Break down the insight into logical claims
        - Only validate factual claims, not opinions
        - For each claim, explicitly reference the evidence source
        - If a claim mentions details not present in any evidence, mark as NotFound
        - Use the LRS data to validate claims about EULR, LR, or ULR
        - The overall insight is valid if no claims are marked as "False"

        Glossary:
        - EULR (Estimated Ultimate Loss Ratio): Values > 0.7 indicate poor program performance
        - LR (Loss Ratio): Ratio of losses to premiums; lower is better
        - ULR (Ultimate Loss Ratio): Similar to EULR but may use different calculation methods
        - LOB (Line of Business): Specific insurance product categories
        - NSA Program: Non-Standard Auto Program for high-risk drivers
        """,
        result_type=InsightValidation,
    )

    # Pass messages list to run_sync
    result = validator.run_sync(messages)
    validation_result = result.data

    # Construct InsightValidation object from the result
    return InsightValidation(
        insight=insight_text,
        program_name=program_name,
        line_of_business=line_of_business,
        premises=validation_result.premises,
        overall_valid=validation_result.overall_valid,
        reasoning=validation_result.reasoning,
    )
