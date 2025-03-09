ASSERTION_PROMPT = """
Examine the following passage and identify the main conclusion. The main conclusionis the primary takeaway or final judgment being made about the data or situation.

For example, in "The book is long-tailed and performance is driven by severe losses, giving high variance to forecasts. The recent underwriting years may be more profitable, driven by a reduction in severity. No major patterns are apparent." The main conclusion is "No major patterns are apparent."

Return the results in JSON format with a single "conclusion" field:

{
    "conclusion": "This is the main conclusion."
}

Guidelines:
1. Focus only on extracting the primary conclusion or final judgment
2. The conclusion is often found at the beginning of the passage, but not always
3. Look for statements that represent the overall assessment or final takeaway
4. The main conclusion often makes a qualitative assessment (e.g., "poorly performing", "improving", "stable")
5. It typically describes the overall state or performance of the program/book being analyzed
6. The conclusion should be a complete sentence that can stand on its own
7. If the conclusion contains evidential clauses, separate them out and keep only the core judgment
    For example, "This is a poorly performing auto liability program (EULR > 0.7)" should become
    "This is a poorly performing auto liability program"
8. Maintain the original wording of the conclusion when possible
9. If multiple conclusions exist, select the most significant or overarching one
10. If there is no clear conclusion in the passage, return "No conclusion found"

The quality of this extraction directly impacts downstream analysis, so accuracy is essential.
        """

""" PROMPTLENGTH

❯ python -c "from pastel.prompts import ASSERTION_PROMPT as text; print(text)" | wc
      31     261    1793
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

""" PROMPTLENGTH

❯ python -c "from pastel.prompts import EVIDENCE_PROMPT as text; print(text.format(conclusion=''))" | wc
      32     286    2260
"""

GRAMMAR_PROMPT = """
Examine the following passage and identify any grammatical errors or misspellings. Only identify objective mistakes. These are meant to be short passages about insurance analytics. Industry abbreviations (EULR, LR, ULR, etc.) and shorthand references are correct.

You are not acting as an Editor. Do not offer style improvements or suggestions. Only return factual grammatical errors. Return the results in JSON format with a single "errors" field:

{{
    "errors": ["Error 1.", "Error 2.", "Error 3."]
}}

Guidelines:
1. Check for grammatical errors, misspellings, and punctuation mistakes
2. Ignore insurance industry abbreviations and technical terms (EULR, LR, ULR, UW, LOB, etc.)
3. Ignore numerical expressions and comparisons (e.g., ">0.7", "2022A vs 2022B")
4. Ignore stylistic issues and informal language
5. Return a list of specific errors found in the passage with clear descriptions
6. If no errors are found, return an empty list: {"errors": []}
7. If the passage is not in English, return an empty list
8. If the passage is not a sentence or is incomplete, return an empty list

"""

""" PROMPTLENGTH

❯ python -c "from pastel.prompts import GRAMMAR_PROMPT as text; print(text)" | wc
      27     188    1286
"""
