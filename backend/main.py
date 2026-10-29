
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.detector import analyze_answer as detect_answer

app = FastAPI(
    title="LLM Hallucination Detection & Explanation",
    description="API for analyzing AI-generated answers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=10000)


@app.get("/")
def home():
    return {
        "message": "LLM Hallucination Detection API is running!",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze")
def analyze_endpoint(request: AnalyzeRequest):
    answer = request.answer.strip()

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="Please provide an answer to analyze.",
        )

    return detect_answer(answer)