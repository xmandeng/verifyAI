from pydantic_ai import Agent

from pastel.models import BaseImage, InsightModel, InsightPlots, PremiseValidation

classifier = Agent(
    # model="anthropic:claude-3-7-sonnet-latest",
    model="anthropic:claude-3-5-sonnet-latest",
    # model="gpt-4-turbo",
    deps_type=InsightModel,
    result_type=list[PremiseValidation],
    model_settings={"temperature": 1},
    system_prompt="""
You are an insurance industry analyst tasked with evaluating the accuracy of insurance insights against data. Your role is to compare statements with the provided image and determine whether the statement is reasonably supported.

Ensure that the statements include the same metrics as the image. Do not confuse dissimilar metrics like price with rates, premiums with losses, etc.

These are very high level & generalized statements. Your consideration should assess the aggregate or overall trend of the reported data, not precise values.

When evaluating statements about "similar performance" or "similar trends," consider:
- Perfect alignment is not required for similarity
- Look for broadly comparable patterns, directions, or ranges
- Minor variations or outliers don't necessarily negate overall similarity
- Consider relative values and general trajectories rather than exact matches

For statements about the severity or frequency of claims specifically:
- Similar performance can mean comparable ranges or overall trajectories
- Lines that follow broadly similar patterns (even with some divergence) can still represent "similar performance"
- The overall story of the data may support similarity claims even with some variation

Provide a balanced assessment that avoids being overly rigid or pedantic. Insurance professionals often speak in generalizations when describing data trends, and your evaluation should reflect this practical perspective.

When evaluating statements, classify them as:
- True: The image reasonably supports the statement
- Partially True: The image shows some support but with notable caveats
- False: The image contradicts the core assertion of the statement
- NotFound: The image doesn't contain relevant information

Return a JSON object with assessment details as previously specified.
""",
)


async def classify_insurance_text(data: str, statements: list[str]) -> list[PremiseValidation]:

    text_statements = ""
    for i, statement in enumerate(statements):
        text_statements += f"{i+1}. {statement}\n"

    result = classifier.run_sync(
        [
            """Evaluate this insurance table (source: lrs.xslx) against the following {count} statements:

From lrs.xslx:
{data}

Statements:
{statements}

Taking the data in aggregate, does it match any statement provided""".format(
                count=len(statements), statements=text_statements, data=data
            ),
        ],
    )

    return [premise for premise in result.data if premise.status != "NotFound"]


async def classify_insurance_image(
    image_obj: BaseImage, statements: list[str]
) -> list[PremiseValidation]:

    text_statements = ""
    for i, statement in enumerate(statements):
        text_statements += f"{i+1}. {statement}\n"

    result = classifier.run_sync(
        [
            """Evaluate this insurance {source} against the following {count} statements:

{statements}
""".format(
                source="image",
                count=len(statements),
                statements=text_statements,
            ),
            image_obj.binary_content,
        ],
    )

    return [premise for premise in result.data if premise.status != "NotFound"]


async def classify_images(images: InsightPlots, statements: list[str]) -> list[PremiseValidation]:

    premises: list[PremiseValidation] = []
    for image_obj in images:
        if not statements:
            break

        premises.extend(await classify_insurance_image(image_obj, statements))

    return premises
