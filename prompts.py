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
- Fix small, obvious syntax issues
- Improve security and code safety
- Preserve original intent as much as possible

Rules:
- Do NOT invent new features
- Do NOT guess missing logic
- You MAY remove insecure behavior (e.g., printing secrets)
- You MAY replace hardcoded secrets with environment variables
- If variable intent is unclear, prefer removal over guessing
- No explanations
- No markdown

CODE:
{code}
"""
