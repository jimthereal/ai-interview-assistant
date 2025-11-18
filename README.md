# AI Interview Assistant

An intelligent interview preparation tool powered by RAG (Retrieval-Augmented Generation) and Large Language Models.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3-green.svg)](https://groq.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [API Documentation](#api-documentation)

---

## About

AI Interview Assistant helps you prepare for technical interviews by analyzing job descriptions and providing personalized practice questions with AI-generated answers and feedback.

**What it does:**
- Analyzes job descriptions to identify key skills and requirements
- Finds relevant interview questions using semantic search
- Generates personalized model answers tailored to the job
- Evaluates your responses with detailed feedback
- Tracks your practice progress over time

**Completely FREE** - No API subscriptions required. Built with Groq's free tier.

---

## Features

### Job Description Analysis
Upload or paste a job description, and the AI will extract:
- Required skills and technologies
- Experience level expectations
- Key focus areas for interview preparation

### Smart Question Matching
- 150+ curated interview questions across technical and behavioral topics
- Semantic search finds the most relevant questions for your target role
- Questions ranked by relevance to job requirements

### AI-Powered Answer Generation
- Context-aware answers tailored to the specific job
- STAR method formatting for behavioral questions
- Professional, articulate responses using Llama 3.3 70B

### Answer Evaluation & Feedback
- Multi-dimensional scoring (clarity, completeness, accuracy, professionalism)
- Specific suggestions for improvement
- Identifies strengths and areas to work on

### Progress Tracking
- View practice history and scores
- Track improvement over time
- Category-wise performance breakdown

---

## Tech Stack

**Backend:**
- Python 3.10+
- FastAPI - Modern, fast web framework
- ChromaDB - Vector database for semantic search
- sentence-transformers - Local embeddings (no API costs)
- Groq API - Free LLM access (Llama 3.3 70B)

**Frontend:**
- React 18+
- TypeScript
- Vite - Fast build tool
- Tailwind CSS - Styling

**Why FastAPI + React?**
- Industry-standard stack used by modern tech companies
- FastAPI provides automatic API documentation and type safety
- React offers responsive, interactive user experience
- Excellent portfolio demonstration of full-stack capabilities

**Total Cost: $0/month**

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm
- Groq API key - [Get FREE key here](https://console.groq.com/) (no credit card required)
- Git (optional)

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/jimthereal/ai-interview-assistant.git
cd ai-interview-assistant
```

**2. Backend Setup:**
```bash
# Create conda environment (RECOMMENDED)
conda create -n ai-interview-assistant python=3.10
conda activate ai-interview-assistant

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your Groq API key
```

**3. Frontend Setup:**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

**Quick Start (RECOMMENDED):**

Open TWO terminals:

**Terminal 1 - Backend:**
```bash
.\start_backend.bat
```

**Terminal 2 - Frontend:**
```bash
.\start_frontend.bat
```

**Manual Start (Alternative):**

**Terminal 1 - Backend:**
```bash
conda activate ai-interview-assistant
python -m uvicorn api.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application

- **Frontend UI:** http://localhost:5173
- **API Swagger Docs:** http://localhost:8000/docs  
- **API ReDoc:** http://localhost:8000/redoc

**Important:** Both backend AND frontend must be running!

---

## How to Use

### 1. Analyze a Job Description
- Navigate to "Job Analysis" page
- Paste a job description from any job posting
- Click "Analyze"
- Review extracted skills and requirements
- View matched interview questions

### 2. Practice Interview Questions
- Go to "Practice" page
- Browse questions or select from job analysis results
- Write your answer
- Click "Generate Model Answer" to see AI-generated example
- Submit your answer for evaluation
- Review detailed feedback and suggestions

### 3. Track Your Progress
- Visit "Dashboard" page
- View practice statistics and scores
- See improvement trends
- Identify areas needing more practice

### 4. Learn Technical Terms
- Use "Term Explainer" for any unfamiliar technical concepts
- Get clear, beginner-friendly explanations

---

## API Documentation

Once the backend is running, view interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

**POST /api/analyze-jd**
- Analyzes job description
- Returns skills, requirements, and matched questions

**POST /api/generate-answer**
- Generates AI model answer for a question
- Takes job context and question as input

**POST /api/evaluate-answer**
- Evaluates user's answer
- Returns scores and detailed feedback

**GET /api/questions**
- Retrieves questions by category or search query

**GET /api/progress**
- Returns user's practice history and statistics

---

## Development

### Project Structure
```
ai-interview-assistant/
├── api/                    # FastAPI backend
│   ├── main.py            # API entry point
│   ├── routes/            # API endpoints
│   └── models/            # Pydantic models
├── src/                   # Core business logic
│   ├── vector_store.py    # ChromaDB operations
│   ├── llm_service.py     # Groq API integration
│   ├── jd_analyzer.py     # Job description analysis
│   └── answer_evaluator.py # Answer evaluation
├── frontend/              # React application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── api/          # API client
│   └── package.json
├── data/
│   ├── interview_questions.json  # Question database
│   └── chroma_db/                # Vector database
├── config/
│   └── config.py          # Configuration
├── requirements.txt       # Python dependencies
└── .env.example          # Environment template
```

### Running Tests
```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

---

## License

This project is open source and available for personal and educational use.

---

## Contact

**Project Repository**: [https://github.com/yourusername/ai-interview-assistant](https://github.com/yourusername/ai-interview-assistant)

For questions or suggestions, please open an issue on GitHub.

---

**Built with Python, FastAPI, React, and Groq AI**
