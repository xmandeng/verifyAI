import pprint

from pydantic_ai import Agent

from pastel.models import GrammarValidation, InsightModel, InsightValidation, PremiseValidation
from pastel.prompts import CONSOLIDATE_PROMPT

consolidator = Agent(
    model="anthropic:claude-3-7-sonnet-latest",
    result_type=InsightValidation,
    # model_settings={"temperature": 1},
    system_prompt=CONSOLIDATE_PROMPT,
)


async def consolidate_evaluations(
    insight: InsightModel, premises: list[PremiseValidation], grammar: GrammarValidation
) -> InsightValidation:

    evaluation_of_evidence = "\n\n".join(
        [f"{pprint.pformat(premise.model_dump())}" for premise in premises]
    )

    evaluation_of_grammar = f"{pprint.pformat(grammar.model_dump())}"

    prompt = f"""
Please evaluate the following and compose a single evaluation.

Insight:

{insight.insight}

Supporting Evidence:

{insight.evidence}

Evaluation of Evidence:

{evaluation_of_evidence}

Grammar:

{evaluation_of_grammar}

"""

    result = consolidator.run_sync(prompt)

    return result.data
