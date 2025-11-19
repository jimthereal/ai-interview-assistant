"""
FastAPI main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import jd_routes, question_routes, answer_routes, progress_routes

app = FastAPI(
    title="AI Interview Assistant API",
    description="Backend API for AI-powered interview assistant",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "http://localhost:3000",
        "https://ai-interview-assistant-xi-smoky.vercel.app",  # Production
        "https://ai-interview-assistant-crg1epup8-jimthereals-projects.vercel.app",  # Preview
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jd_routes.router, prefix="/api", tags=["Job Description"])
app.include_router(question_routes.router, prefix="/api", tags=["Questions"])
app.include_router(answer_routes.router, prefix="/api", tags=["Answers"])
app.include_router(progress_routes.router, prefix="/api", tags=["Progress"])


@app.get("/")
async def root():
    return {
        "message": "AI Interview Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "ok"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
