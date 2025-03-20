"""PROMPT INFO

{
    "input_tokens": 744,
    "output_tokens": 79,
}

❯ python -c "from verifyai.prompts import GRAMMAR_PROMPT as text; print(text)" | wc
      27     188    1286
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
