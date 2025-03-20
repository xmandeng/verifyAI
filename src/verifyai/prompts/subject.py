"""PROMPT INFO

{
    "completion_tokens": 24,
    "prompt_tokens": 472,
    "total_tokens": 496,
}

❯ python -c "from verifyai.prompts import CONCLUSION_PROMPT as text; print(text)" | wc
      31     261    1793

"""

CONCLUSION_PROMPT = """
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
