# LLM Hallucination Detection & Explanation

A Python-based web application that analyzes AI-generated answers, extracts individual claims, and evaluates them against a small demo evidence base using rule-based checks and semantic similarity.

## Overview

Large Language Models (LLMs) can sometimes generate incorrect or unsupported information. This project demonstrates an explainable approach to identifying claims that require further verification.

Each claim is classified into one of three categories: Supported, Contradicted, or Not Enough Evidence.

## Features

- Analyze AI-generated text.
- Extract individual claims from an answer.
- Classify claims as Supported, Contradicted, or Not Enough Evidence.
- Match claims against predefined evidence.
- Use semantic similarity to identify potentially relevant evidence.
- Display matching evidence and explanations.
- Show semantic similarity scores when available.
- Calculate a demo risk indicator.
- Display claim statistics and a visual risk bar.
- Validate user input and handle errors.
- Include automated tests using pytest.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Sentence Transformers
- HTML
- CSS
- JavaScript
- Pytest

## Project Structure

```text
llm-hallucination-detection/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── detector.py
│   └── semantic_matcher.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   ├── test_api.py
│   ├── test_detector.py
│   └── test_semantic_matcher.py
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/anurag9785/llm-hallucination-detection.git
cd llm-hallucination-detection
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
python -m pip install fastapi "uvicorn[standard]" pydantic pytest httpx sentence-transformers
```

### 5. Start the Backend

```bash
python -m uvicorn backend.main:app --reload
```

The API runs at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

Keep the backend running while using the frontend.

### 6. Open the Frontend

Open `frontend/index.html` in your browser or use the VS Code Live Server extension.

## Run Automated Tests

Run this command from the project root:

```bash
python -m pytest -v
```

## How It Works

1. The user submits an AI-generated answer.
2. The backend separates the answer into individual claims.
3. Each claim is checked against predefined evidence and contradiction rules.
4. The semantic matcher identifies potentially relevant evidence using sentence embeddings.
5. The detector assigns a classification and provides an explanation.
6. The frontend displays the results, evidence, statistics, and demo risk indicator.

## Classification Categories

- **Supported:** The claim exactly matches a fact in the demo evidence base.
- **Contradicted:** The claim conflicts with a predefined contradiction rule.
- **Not Enough Evidence:** The available evidence does not establish whether the claim is correct.

Semantic similarity alone does not establish factual accuracy.

## Important Limitations

This is an educational prototype, not a validated hallucination detection system.

- The evidence base contains only a limited number of predefined facts.
- Contradiction detection uses predefined rules.
- Semantic similarity identifies related text but cannot independently verify facts.
- Unsupported claims are not necessarily false.
- The demo risk indicator is not a calibrated probability of hallucination.
- Results should be independently verified using reliable sources.

## Future Improvements

- Integrate trusted external knowledge sources.
- Expand the evidence database.
- Add source citations and evidence retrieval.
- Improve contradiction detection.
- Evaluate performance using a labeled dataset.
- Add support for larger documents and multiple languages.

## Author

Developed as an educational project to explore AI reliability, evidence verification, semantic matching, and explainable claim analysis.
