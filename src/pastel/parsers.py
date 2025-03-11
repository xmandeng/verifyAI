from pydantic_ai import Agent, RunContext
from pydantic_ai.models import KnownModelName

from pastel.models import ClaimModel, GrammarValidation, InsightModel
from pastel.prompts import EVIDENCE_PROMPT, GRAMMAR_PROMPT, SUBJECT_PROMPT

OPENAI_MODEL: KnownModelName = "openai:gpt-4o-mini"
ANTHROPIC_MODEL: KnownModelName = "anthropic:claude-3-5-sonnet-latest"

claim_agent = Agent(
    model=OPENAI_MODEL,
    system_prompt=SUBJECT_PROMPT,
    result_type=ClaimModel,
)


async def parse_assertion(insight: str) -> ClaimModel:
    result = claim_agent.run_sync(insight)
    return result.data


evidence_agent = Agent(
    model=OPENAI_MODEL,
    deps_type=ClaimModel,
    result_type=InsightModel,
)


@evidence_agent.system_prompt
def build_evidence_prompt(ctx: RunContext[ClaimModel]) -> str:
    return EVIDENCE_PROMPT.format(conclusion=ctx.deps.conclusion)


async def parse_evidence(claim: ClaimModel, insight: str) -> InsightModel:
    result = evidence_agent.run_sync(insight, deps=claim)
    return InsightModel(conclusion=claim.conclusion, evidence=result.data.evidence)


grammar_agent = Agent(
    model=ANTHROPIC_MODEL,
    system_prompt=GRAMMAR_PROMPT,
    result_type=GrammarValidation,
)


async def check_grammar(insight: str) -> GrammarValidation:
    result = grammar_agent.run_sync(insight)
    return result.data
