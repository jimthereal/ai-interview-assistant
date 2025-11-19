# AI Interview Assistant

AI-powered interview preparation tool using RAG and Large Language Models to analyze job descriptions and provide personalized practice questions with detailed feedback.

## About

**What it does:**
- Analyzes job descriptions (paste text, upload files, or scrape URLs)
- Matches relevant interview questions from 150+ curated database
- Generates AI-powered model answers tailored to the job
- Evaluates your responses with detailed scoring and feedback
- Tracks practice progress and improvement trends

**Tech Stack:** Python, FastAPI, React, ChromaDB, Groq API (Free)

---

## Features

### Job Description Analysis 📄
**Multiple input methods:**
- 📝 **Paste Text** - Copy and paste job descriptions
- 📄 **Upload File** - Upload PDF or Word documents (.pdf, .docx)
- 🔗 **Paste URL** - Scrape job postings from websites (JobStreet, LinkedIn, etc.)

**AI extracts:**
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

**Three ways to input job descriptions:**

**Option A: Paste Text**
- Navigate to "Job Analysis" page
- Click "📝 Paste Text" tab
- Paste job description
- Click "Analyze"

**Option B: Upload File (NEW!)**
- Navigate to "Job Analysis" page
- Click "📄 Upload File" tab
- Upload PDF or Word document
- Click "Analyze"

**Option C: Paste URL (NEW!)**
- Navigate to "Job Analysis" page
- Click "🔗 Paste URL" tab
- Paste job posting URL (e.g., from JobStreet, LinkedIn)
- Click "Analyze"

**Results:**
- Review extracted skills and requirements
- View matched interview questions
- Click any question to start practicing

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

## Deployment

Want to host this online? Check out the [DEPLOYMENT.md](DEPLOYMENT.md) guide for:
- ✅ Free hosting options (Vercel + Render)
- ✅ Step-by-step deployment instructions
- ✅ Cost comparisons
- ✅ Production best practices

**Note**: You do NOT need your PC running 24/7. Deploy to cloud services instead!

---

**Built with Python, FastAPI, React, and Groq AI**