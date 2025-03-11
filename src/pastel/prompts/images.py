IMAGE_PROMPT = """
Classify this insurance visualization image into exactly one of these four categories:

1. pricing - A Time series chart showing pricing changes over time, often showing premium trends
2. severity - A Time series chart showing claim severity metrics, often showing ratios of large claims to total claims
3. frequency - A Time series chart showing claim frequency over time, measuring how often claims are filed
4. cuts - A scatter plot chart showing business segment analysis, breaking down metrics by categories/segments

Return ONLY the category name as a single word: "pricing", "severity", "frequency", or "cuts".
Do not include any other text, explanation, or punctuation in your response.
"""
