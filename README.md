# AI Interview Assistant

An intelligent .

AI-powered interview assistant powered by RAG (Retrieval-Augmented Generation) and LLMs (Large Language Models) to analyze job descriptions and provide personalized practice questions with detailed feedback.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3-green.svg)](https://groq.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [How to Use](#how-to-use)

---

## About

**What it does:**
- Analyzes job descriptions (paste text, upload files, or scrape URLs)
- Matches relevant interview questions from 150+ curated database
- Generates AI-powered model answers tailored to the job
- Evaluates your responses with detailed scoring and feedback
- Tracks practice progress and improvement trends

---

## Features

### Job Description Analysis
**Multiple input methods:**
- **Paste Text** - Copy and paste job descriptions
- **Upload File** - Upload PDF or Word documents (.pdf, .docx)
- **Paste URL** - Scrape job postings from websites (JobStreet, LinkedIn, etc.)

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

**Built with Python, FastAPI, React, and Groq AI**