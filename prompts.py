def review_prompt(code: str, language: str) -> str:
    return f"""
You are a senior software engineer reviewing {language} code.

Analyze the code and group issues into categories.

Use ONLY this format:

Security:
• issue
• issue
→ Suggestion: short fix

Performance:
• issue
→ Suggestion: short fix

Code Quality:
• issue
• issue
→ Suggestion: short fix

Rules:
- Max 2 issues per category
- Suggestions must be 1 line
- No explanations
- Omit empty categories

CODE:
{code}
"""


def rewrite_prompt(code: str, language: str) -> str:
    return f"""
You are a senior {language} developer.

Rewrite the code ONLY if it is valid.

Rules:
- Preserve the original logic EXACTLY
- Do NOT invent new functions, variables, or behavior
- Do NOT guess missing logic
- Do NOT add features
- If the code is invalid or incomplete, return it unchanged
- No explanations
- No markdown formatting

CODE:
{code}
"""
