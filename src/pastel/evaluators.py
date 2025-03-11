from pydantic_ai import Agent, RunContext
from pydantic_ai.models import KnownModelName

from pastel.models import AssertionModel, InsightModel
from pastel.prompts import EVIDENCE_PROMPT

OPENAI_MODEL: KnownModelName = "openai:gpt-4o-mini"
ANTHROPIC_MODEL: KnownModelName = "anthropic:claude-3-5-sonnet-latest"


eval_agent = Agent(
    model=OPENAI_MODEL,
    deps_type=InsightModel,
    result_type=InsightModel,
)


@eval_agent.system_prompt
def build_evidence_prompt(ctx: RunContext[AssertionModel]) -> str:
    return EVIDENCE_PROMPT.format(conclusion=ctx.deps.conclusion)


async def parse_evidence(claim: InsightModel, insight: str) -> InsightModel:
    result = eval_agent.run_sync(insight, deps=claim)
    return InsightModel(conclusion=claim.conclusion, evidence=result.data.evidence)
