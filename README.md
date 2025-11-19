# 🤖 AI Interview Assistant

> Modern full-stack interview preparation platform powered by AI, deployed on cloud infrastructure

[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](https://ai-interview-assistant-xi-smoky.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)
[![Deployed](https://img.shields.io/badge/Deployed-Vercel%20%2B%20Render-blueviolet)](https://vercel.com)

## 🌟 Overview

AI-powered interview assistant that analyzes job descriptions and provides personalized practice questions with intelligent feedback. Built with modern web technologies and deployed on cloud platforms for global accessibility.

**🚀 Live Demo:** [https://ai-interview-assistant-xi-smoky.vercel.app](https://ai-interview-assistant-xi-smoky.vercel.app)

## ✨ Features

### 📄 **Multi-Source Job Description Analysis**
- **Paste Text** - Direct input of job postings
- **Upload Files** - PDF & Word documents (.pdf, .docx)
- **Scrape URLs** - Extract from job sites (JobStreet, LinkedIn, Indeed)

### 🎯 **Smart Question Matching**
- 150+ curated technical & behavioral questions
- AI-powered relevance ranking
- 11 categories (Python, ML, System Design, Cloud, etc.)

### 🤖 **AI-Powered Features**
- **Answer Generation** - Context-aware model answers using Llama 3.3 70B
- **Answer Evaluation** - Multi-dimensional scoring (clarity, completeness, accuracy)
- **Term Explainer** - Beginner-friendly technical concept explanations

### 📊 **Progress Tracking**
- Practice history with timestamps
- Performance trends and analytics
- Category-wise breakdown
- Improvement suggestions

## 🛠️ Tech Stack

### **Backend**
- **Framework:** FastAPI (Python 3.10+)
- **AI/LLM:** Groq API (Llama 3.3 70B) - FREE tier
- **Vector Search:** ChromaDB (dev) / Keyword Search (production)
- **Hosting:** Render (auto-deploy from GitHub)

### **Frontend**
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite 5
- **Styling:** Tailwind CSS 3
- **State Management:** Zustand
- **Routing:** React Router 6
- **Hosting:** Vercel (edge network)

### **Document Processing**
- **PDF Parsing:** PyPDF2
- **Word Documents:** python-docx
- **Web Scraping:** BeautifulSoup4

### **Deployment Architecture**
```
User Request
    ↓
Vercel Edge (Frontend - React)
    ↓
Render Cloud (Backend - FastAPI)
    ↓
Groq API (LLM Inference)
```

## 💡 How to Use

### 1️⃣ **Analyze Job Description**
Choose your input method:
- **Text:** Paste job description directly
- **File:** Upload PDF/DOCX document
- **URL:** Scrape from job sites

Get AI-extracted skills and matched questions.

### 2️⃣ **Practice Questions**
- Browse 150+ questions by category
- Select questions from job analysis
- Write your answer
- Get AI-generated model answer
- Receive detailed evaluation

### 3️⃣ **Track Progress**
- View practice history
- Monitor improvement trends
- Analyze performance by category
- Get personalized suggestions

### 4️⃣ **Learn Concepts**
- Use Term Explainer for technical jargon
- Get clear, beginner-friendly explanations
- Understand industry terminology

## 🏗️ Architecture Highlights

### **Production Optimizations**
- **Memory-Efficient:** Keyword search for low-memory environments
- **Fast Startup:** ~5 seconds (vs 60s with ML models)
- **Adaptive:** Switches between dev (embeddings) and prod (keywords) modes
- **Scalable:** Stateless backend, edge-deployed frontend

### **Key Design Decisions**
- **RAG Pattern:** Retrieval-Augmented Generation for context-aware answers
- **Separation of Concerns:** Backend API + Frontend SPA
- **Cloud-Native:** Designed for serverless/container deployments
- **Free Tier Optimized:** Runs on free Render + Vercel tiers

## 🌐 Deployment

This project is production-ready and deployed on:
- **Frontend:** Vercel (Global CDN)
- **Backend:** Render (Cloud containers)

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome! Feel free to open issues or submit pull requests.

## 🙏 Acknowledgments

- **Groq** - Free LLM API access
- **Vercel** - Frontend hosting
- **Render** - Backend hosting
- **FastAPI** - Modern Python web framework
- **React** - UI library

---

**Built with ❤️ using Python, FastAPI, React, and AI**

*Deployed on modern cloud infrastructure for global accessibility*
