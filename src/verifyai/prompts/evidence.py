"""PROMPT INFO

{
    "completion_tokens": 78,
    "prompt_tokens": 543,
    "total_tokens": 621,
}

❯ python -c "from pastel.prompts import EVIDENCE_PROMPT as text; print(text.format(conclusion=''))" | wc
      32     286    2260
"""

EVIDENCE_PROMPT = """
You are an expert in insurance analytics. Examine the following passage and identify all supporting evidence for the given conclusion: "{conclusion}"

Your task is to extract all statements from the passage that are not the conclusion. The conclusion may be embedded within the passage, possibly intertwined with its supporting evidence.

Return the results in JSON format with the "conclusion" field and an "evidence" array containing all other statements:

{{
    "conclusion": "The conclusion as provided.",
    "evidence": ["Supporting evidence 1.", "Supporting evidence 2.", "Supporting evidence 3."]
}}

Guidelines:
1. Extract all statements that provide facts, data, observations, or reasoning that support the conclusion
2. Do not include the conclusion itself as supporting evidence - the conclusion cannot be its own evidence
3. Maintain text in parentheses, e.g. "This is a well-performing trucking program (EULR < 0.7) consisting predominantly of auto liability risk (LOB 19.4, 21.2)."
4. Maintain the exact wording of the evidence
5. If the conclusion itself contains supporting evidence, separate that evidence into distinct statements
For example, from "This is a poorly performing auto liability program (EULR > 0.7) with stable pricing":
- Extract "The Expected Ultimate Loss Ratio (EULR) is greater than 0.7."
- Extract "The program has stable pricing."
6. Split compound evidence statements into separate items when they contain distinct facts
For example, "There is similar performance for frequency and severity of claims" should become:
- "There is similar performance for frequency of claims."
- "There is similar performance for severity of claims."
7. If the passage contains information not directly supporting the conclusion, still include it as evidence
8. Maintain the original meaning and context throughout your analysis

The quality of this extraction directly impacts downstream analysis, so thoroughness and accuracy are essential.
        """
