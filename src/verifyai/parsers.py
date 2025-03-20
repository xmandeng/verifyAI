from pydantic_ai import Agent, RunContext
from pydantic_ai.models import KnownModelName

from verifyai.models import AssertionModel, GrammarValidation, InputModel, InsightModel
from verifyai.prompts import CONCLUSION_PROMPT, EVIDENCE_PROMPT, GRAMMAR_PROMPT

OPENAI_MODEL: KnownModelName = "openai:gpt-4o-mini"
ANTHROPIC_MODEL: KnownModelName = "anthropic:claude-3-5-sonnet-latest"

assertion_agent = Agent(
    model=OPENAI_MODEL,
    system_prompt=CONCLUSION_PROMPT,
    result_type=AssertionModel,
    deps_type=InputModel,
)


async def parse_assertion(input_model: InputModel) -> AssertionModel:
    result = assertion_agent.run_sync(input_model.insight)
    return AssertionModel(conclusion=result.data.conclusion, **input_model.model_dump())


evidence_agent = Agent(
    model=OPENAI_MODEL,
    deps_type=AssertionModel,
    result_type=InsightModel,
)


@evidence_agent.system_prompt
def build_evidence_prompt(ctx: RunContext[AssertionModel]) -> str:
    return EVIDENCE_PROMPT.format(conclusion=ctx.deps.conclusion)


async def parse_evidence(assertion: AssertionModel) -> InsightModel:
    result = evidence_agent.run_sync(assertion.insight, deps=assertion)
    return InsightModel(
        evidence=result.data.evidence,
        **assertion.model_dump(),
    )


grammar_agent = Agent(
    model=ANTHROPIC_MODEL,
    system_prompt=GRAMMAR_PROMPT,
    result_type=GrammarValidation,
)


async def check_grammar(input_data: InputModel | InsightModel) -> GrammarValidation:
    result = grammar_agent.run_sync(input_data.insight)
    return result.data
