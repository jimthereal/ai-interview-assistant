# Project Structure

```
ai-interview-assistant/
│
├── README.md                    # Main documentation
├── DEPLOYMENT.md                # Deployment guide
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── start_backend.bat            # Quick start script for backend (Windows)
├── start_frontend.bat           # Quick start script for frontend (Windows)
│
├── api/                         # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point, CORS config
│   │
│   ├── models/                  # Data models & schemas
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models for API requests/responses
│   │
│   └── routes/                  # API route handlers
│       ├── __init__.py
│       ├── jd_routes.py         # Job description analysis endpoints
│       ├── question_routes.py   # Question retrieval endpoints
│       ├── answer_routes.py     # Answer generation & evaluation endpoints
│       └── progress_routes.py   # Progress tracking endpoints
│
├── config/                      # Configuration
│   ├── __init__.py
│   └── config.py                # App configuration, environment variables
│
├── src/                         # Core Business Logic
│   ├── __init__.py
│   ├── llm_service.py           # Groq API integration, LLM calls
│   ├── jd_analyzer.py           # Job description analysis logic
│   ├── answer_evaluator.py     # Answer evaluation & scoring
│   ├── vector_store.py          # ChromaDB vector database interface
│   └── content_extractor.py    # PDF/DOCX/URL content extraction (NEW)
│
├── data/                        # Data Storage
│   ├── interview_questions.json # 150 curated interview questions
│   └── chroma_db/               # ChromaDB vector database (auto-generated)
│
├── frontend/                    # React Frontend
│   ├── package.json             # Frontend dependencies
│   ├── vite.config.ts           # Vite build configuration
│   ├── tailwind.config.js       # Tailwind CSS config
│   ├── tsconfig.json            # TypeScript configuration
│   ├── index.html               # Entry HTML file
│   │
│   ├── src/                     # Frontend source code
│   │   ├── main.tsx             # React app entry point
│   │   ├── App.tsx              # Main app component with routing
│   │   ├── index.css            # Global styles
│   │   │
│   │   ├── api/                 # API client
│   │   │   └── client.ts        # Axios API calls to backend
│   │   │
│   │   ├── components/          # Reusable UI components
│   │   │   ├── Layout.tsx       # App layout with sidebar navigation
│   │   │   ├── Sidebar.tsx      # Navigation sidebar
│   │   │   ├── Loading.tsx      # Loading spinner component
│   │   │   └── ScoreRing.tsx    # Circular score visualization
│   │   │
│   │   ├── pages/               # Page components (routes)
│   │   │   ├── Home.tsx         # Landing/home page
│   │   │   ├── JobAnalysis.tsx  # Job description analysis page (3 tabs)
│   │   │   ├── PracticeList.tsx # Question list page (NEW)
│   │   │   ├── PracticeQuestion.tsx # Individual question practice (NEW)
│   │   │   ├── Progress.tsx     # Progress dashboard (UPDATED)
│   │   │   └── Explainer.tsx    # Technical term explainer
│   │   │
│   │   ├── store/               # State management
│   │   │   └── index.ts         # Zustand store (global state)
│   │   │
│   │   └── types/               # TypeScript type definitions
│   │       └── index.ts         # Shared types/interfaces
│   │
│   └── dist/                    # Build output (generated, not in Git)
│
└── tests/ (Optional)            # Test files
    ├── test_endpoints.py        # API endpoint tests
    ├── test_new_features.py     # Feature tests
    └── create_sample_pdf.py     # Sample PDF generator for testing

```

## Key Files Explained

### Backend Core Files

**`api/main.py`**
- FastAPI application initialization
- CORS middleware configuration
- Route registration
- Startup/shutdown events

**`src/llm_service.py`**
- Groq API integration
- LLM prompt templates
- Response parsing

**`src/jd_analyzer.py`**
- Job description parsing
- Skill extraction
- Search query generation

**`src/answer_evaluator.py`**
- Answer scoring logic
- Feedback generation
- Multi-dimensional evaluation

**`src/vector_store.py`**
- ChromaDB initialization
- Embedding generation
- Semantic search
- Question retrieval

**`src/content_extractor.py`** *(NEW)*
- PDF text extraction (PyPDF2)
- Word document parsing (python-docx)
- Web scraping (BeautifulSoup4)
- Content validation

### Frontend Core Files

**`frontend/src/App.tsx`**
- React Router setup
- Route definitions
- App-level components

**`frontend/src/store/index.ts`**
- Zustand state management
- Global state: job analysis, practice history
- State persistence

**`frontend/src/pages/JobAnalysis.tsx`** *(UPDATED)*
- 3-tab interface (Text / File / URL)
- File upload with drag & drop
- URL validation and scraping
- Job description analysis

**`frontend/src/pages/PracticeList.tsx`** *(NEW)*
- Question listing page
- Category filter
- Search functionality
- Lazy loading (20 questions at a time)

**`frontend/src/pages/PracticeQuestion.tsx`** *(NEW)*
- Individual question practice
- Answer input
- Model answer generation
- Answer evaluation
- Practice history tracking

**`frontend/src/pages/Progress.tsx`** *(UPDATED)*
- Dashboard with statistics
- Practice history display
- Performance trends
- Category breakdown
- Smart suggestions

### Configuration Files

**`.env.example`**
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

**`requirements.txt`**
- Python dependencies
- FastAPI, Uvicorn
- ChromaDB, sentence-transformers
- PyPDF2, python-docx, python-multipart (NEW)
- beautifulsoup4, requests

**`frontend/package.json`**
- React, TypeScript, Vite
- Tailwind CSS
- Axios, React Router
- Zustand
- marked (markdown parser) (NEW)

## Data Flow

### 1. Job Description Analysis
```
User Input (Text/File/URL)
    ↓
Content Extraction (if File/URL)
    ↓
JD Analyzer (Extract skills, role, level)
    ↓
Vector Store Search (Find relevant questions)
    ↓
Return: Analysis + Matched Questions
```

### 2. Practice Question
```
User selects question
    ↓
Generate Model Answer (LLM Service)
    ↓
User writes answer
    ↓
Evaluate Answer (Answer Evaluator + LLM)
    ↓
Store in Practice History (Zustand)
    ↓
Display scores & feedback
```

### 3. Progress Dashboard
```
Read Practice History (Zustand store)
    ↓
Calculate statistics locally
    ↓
Display: Scores, trends, category breakdown
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.10+
- **LLM**: Groq API (Llama 3.3 70B)
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **File Parsing**: PyPDF2, python-docx
- **Web Scraping**: BeautifulSoup4, requests

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **Build Tool**: Vite 5+
- **Styling**: Tailwind CSS 3+
- **Routing**: React Router 6+
- **State**: Zustand 4+
- **HTTP Client**: Axios
- **Markdown**: marked

### Development Tools
- **Python Env**: Conda (recommended) or venv
- **Node**: Node.js 18+
- **Package Manager**: npm

## Important Notes

### What's in Git
✅ Source code
✅ Configuration examples (.env.example)
✅ Documentation
✅ Test scripts
✅ Starter scripts

### What's NOT in Git (`.gitignore`)
❌ `.env` (contains secrets)
❌ `node_modules/` (installed via npm)
❌ `__pycache__/` (Python cache)
❌ `frontend/dist/` (build output)
❌ `data/chroma_db/` (database files)
❌ Root `package.json` and `package-lock.json` (unnecessary)

### File Counts
- **Backend Files**: ~20 Python files
- **Frontend Files**: ~15 TypeScript/React files
- **Total Questions**: 150 (in `data/interview_questions.json`)
- **Lines of Code**: ~5000+ lines

## Recent Updates (November 2025)

### New Features
- ✅ File upload support (PDF/DOCX)
- ✅ URL scraping for job postings
- ✅ 3-tab input interface in Job Analysis
- ✅ Practice page redesign (List → Detail view)
- ✅ Progress dashboard local state
- ✅ Practice history persistence

### New Files
- `src/content_extractor.py` - Content extraction utilities
- `frontend/src/pages/PracticeList.tsx` - Question list page
- `frontend/src/pages/PracticeQuestion.tsx` - Question detail page
- `DEPLOYMENT.md` - Deployment guide
- `PROJECT_STRUCTURE.md` - This file

### Updated Files
- `api/routes/jd_routes.py` - Added file/URL endpoints
- `frontend/src/pages/JobAnalysis.tsx` - 3-tab interface
- `frontend/src/pages/Progress.tsx` - Local state calculation
- `frontend/src/api/client.ts` - New API methods
- `frontend/src/store/index.ts` - Practice history tracking
- `requirements.txt` - Added PyPDF2, python-docx, python-multipart
- `README.md` - Updated features section

---

**Last Updated**: November 19, 2025
