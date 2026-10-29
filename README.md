
# LLM Hallucination Detection & Explanation

A Python-based web application that analyzes AI-generated answers, splits them into individual claims, and checks them against a small demo evidence base.

## Overview

Large Language Models (LLMs) can sometimes generate information that is incorrect or unsupported. This project demonstrates a basic, rule-based approach to identifying claims that need further verification.

## Features

- Analyze AI-generated text.
- Extract individual claims from an answer.
- Classify claims as Supported, Contradicted, or Not Enough Evidence.
- Display matching evidence and explanations.
- Calculate a demo risk indicator.
- Show claim statistics and a visual risk bar.
- Provide input validation and error messages.
- Include automated tests using pytest.

## Tech Stack

- Python
- FastAPI
- Pydantic
- HTML
- CSS
- JavaScript
- Pytest

## Project Structure

```text
LLM Hallucination Detection & Explanation/
├── backend/
│   ├── main.py
│   └── detector.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   └── test_detector.py
├── data/
├── .venv/
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "LLM Hallucination Detection & Explanation"
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install fastapi "uvicorn[standard]" pydantic pytest
```

### 4. Start the backend

```bash
python -m uvicorn backend.main:app --reload
```

The API runs at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### 5. Open the frontend

Open `frontend/index.html` in a browser, or use the VS Code Live Server extension.

Keep the backend running while using the frontend.

## Run Tests

```bash
python -m pytest -v
```

## How It Works

1. The user submits an AI-generated answer.
2. The backend separates the answer into claims.
3. Each claim is compared with predefined demo evidence and contradiction rules.
4. The application assigns a label and provides an explanation.
5. The frontend displays the results, statistics, and demo risk indicator.

## Important Limitations

This is an educational prototype, not a validated hallucination detection system.

- The evidence base contains only a few predefined facts.
- The detector relies on simple rules and exact text matching.
- Unsupported claims are not necessarily false.
- The demo risk indicator is not a calibrated probability of hallucination.
- Results should be independently verified using reliable sources.

## Future Improvements

- Integrate trusted external knowledge sources.
- Improve semantic claim matching.
- Add source citations and evidence retrieval.
- Expand automated API tests.
- Evaluate accuracy using a labeled dataset.

## Author

Developed as an educational project to explore AI reliability, evidence verification, and explainable claim analysis.
