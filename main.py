from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai import ask_llm
from prompts import review_prompt, rewrite_prompt

app = FastAPI(
    title="CodeRefine API",
    docs_url="/docs",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str
    language: str

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/review")
def review_code(data: CodeInput):
    prompt = review_prompt(data.code, data.language)
    result = ask_llm(prompt)
    return {"review": result}

@app.post("/rewrite")
def rewrite_code(data: CodeInput):

    # Empty input
    if not data.code.strip():
        return {
            "optimized_code": "⚠️ Please enter code before requesting optimization."
        }

    # Try strict validation first (Python only)
    if data.language.lower() == "python":
        try:
            compile(data.code, "<string>", "exec")
            # Code is valid → normal optimization
            prompt = rewrite_prompt(data.code, data.language)
            optimized_code = ask_llm(prompt)
            return {"optimized_code": optimized_code}

        except SyntaxError:
            # Attempt small, safe correction
            fix_prompt = f"""
You are a Python syntax corrector.

Fix ONLY small, obvious syntax errors.
Examples:
- Print → print
- Missing parentheses
- Case sensitivity issues

Rules:
- Do NOT refactor
- Do NOT add logic
- Do NOT change behavior
- If unsure, return original code

Return ONLY corrected code.

CODE:
{data.code}
"""
            corrected = ask_llm(fix_prompt)

            # Try compiling corrected version
            try:
                compile(corrected, "<string>", "exec")
                # Now optimize corrected code
                optimize_prompt = rewrite_prompt(corrected, data.language)
                optimized_code = ask_llm(optimize_prompt)
                return {"optimized_code": optimized_code}
            except SyntaxError:
                return {
                    "optimized_code":
                    "❌ Code has ambiguous syntax errors. Please fix them manually."
                }


