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

    # ✅ Empty input check
    if not data.code.strip():
        return {
            "optimized_code": "⚠️ Please enter code before requesting optimization."
        }

    # ✅ Syntax validation for Python
    if data.language.lower() == "python":
        try:
            compile(data.code, "<string>", "exec")
        except SyntaxError:
            return {
                "optimized_code":
                "❌ Syntax Error detected.\nPlease fix the code before requesting optimization."
            }

    # ✅ Call AI only if input is valid
    prompt = rewrite_prompt(data.code, data.language)
    optimized_code = ask_llm(prompt)

    return {"optimized_code": optimized_code}


