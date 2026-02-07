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

Rewrite the code to be:
- Secure
- Clean
- Production-ready

Rules:
- Do NOT hardcode secrets
- Prefer environment variables
- Avoid printing sensitive data
- Add minimal comments only

Return ONLY the rewritten code.

CODE:
{code}
"""