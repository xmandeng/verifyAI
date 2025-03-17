from pydantic_ai import Agent

from pastel.models import BaseDocument, PremiseValidation

# Create an AI agent for insurance analysis
classifier = Agent(
    model="gpt-4-turbo",
    # deps_type=InsightModel,
    result_type=list[PremiseValidation],
    # model_settings={"temperature": 1},
    system_prompt="""
You are an insurance industry analyst tasked with evaluating the accuracy of insurance insights against visual data.
Your role is to compare statements with the provided **PDF report containing charts and graphs** and determine whether the statements are supported.

- Look at the **graphs, trends, and data visualizations** in the PDF.
- When evaluating statements about "similar performance" or "similar trends," consider:
    - General patterns, trajectories, and relative values
    - Small variations do not necessarily contradict similarity
    - Avoid confusing different metrics like pricing vs. frequency

Classify statements as:
- **True**: The PDF’s visuals support the statement.
- **Partially True**: The PDF shows partial support, but with caveats.
- **False**: The PDF’s visuals contradict the statement.
- **NotFound**: The PDF does not contain relevant data.

Return a **JSON object** with your classification results.
""",
)


async def classify_insurance_pdf(
    pdf_obj: BaseDocument,
) -> list[PremiseValidation]:

    result = classifier.run_sync(
        [
            """Evaluate the provided PDF report, focusing on the visual elements such as charts, graphs, and data visualizations.

Carefully compare these visuals with the given statements and classify each statement as follows:
- True: The visuals in the PDF fully support the statement.
- Partially True: The visuals provide some support for the statement, but with notable caveats.
- False: The visuals contradict the statement.
- NotFound: The PDF does not contain relevant information to support or refute the statement.
""",
            pdf_obj.binary_content,  # Attach the entire PDF
        ],
    )

    return [premise for premise in result.data if premise.status != "NotFound"]
