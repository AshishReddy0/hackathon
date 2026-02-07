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

Your task:
- Fix small, obvious syntax issues IF present
- Then optimize the code

Rules:
- Preserve original logic
- Do NOT invent new logic or functions
- Do NOT guess missing intent
- Only correct errors with ONE clear fix
- If the code is ambiguous, return it unchanged
- No explanations
- No markdown

CODE:
{code}
"""
