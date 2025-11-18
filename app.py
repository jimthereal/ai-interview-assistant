"""
Main Streamlit Application for AI Interview Assistant
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# Import custom modules
from src.vector_store import VectorStore, initialize_vector_store
from src.llm_service import LLMService
from src.jd_analyzer import JDAnalyzer
from src.answer_evaluator import AnswerEvaluator, ProgressTracker
from config.config import Config

# Page configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'llm_service' not in st.session_state:
        st.session_state.llm_service = LLMService()
    if 'jd_analyzer' not in st.session_state:
        st.session_state.jd_analyzer = JDAnalyzer()
    if 'evaluator' not in st.session_state:
        st.session_state.evaluator = AnswerEvaluator()
    if 'progress_tracker' not in st.session_state:
        st.session_state.progress_tracker = ProgressTracker()
    
    if 'current_jd_analysis' not in st.session_state:
        st.session_state.current_jd_analysis = None
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = []
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 0
    if 'practice_history' not in st.session_state:
        st.session_state.practice_history = []
    if 'generated_answer' not in st.session_state:
        st.session_state.generated_answer = ""

init_session_state()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page:",
    ["Home", "Job Description Analysis", "Practice Interview", 
     "Progress Dashboard", "Term Explainer", "About"]
)

# Initialize vector store
if st.session_state.vector_store is None:
    with st.spinner("Initializing knowledge base..."):
        try:
            st.session_state.vector_store = initialize_vector_store()
            stats = st.session_state.vector_store.get_stats()
            st.sidebar.success(f"Loaded {stats['total_questions']} questions")
        except Exception as e:
            st.sidebar.error(f"Error loading questions: {str(e)}")

# ========== HOME PAGE ==========
if page == "Home":
    st.markdown("<h1 class='main-header'>AI Interview Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Your Personal AI-Powered Interview Preparation Tool</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📄 Smart Analysis")
        st.write("Upload job descriptions and get instant insights on required skills, technologies, and likely interview questions.")
        
    with col2:
        st.markdown("### 🤖 AI-Powered Prep")
        st.write("Practice with personalized questions retrieved using RAG technology and get AI-generated model answers.")
        
    with col3:
        st.markdown("### 📊 Track Progress")
        st.write("Monitor your improvement with detailed analytics and personalized recommendations.")
    
    st.markdown("---")
    
    st.markdown("### 🚀 Quick Start Guide")
    st.markdown("""
    1. **Analyze Job Description**: Paste a job posting to extract key requirements
    2. **Get Relevant Questions**: Our RAG system finds the most relevant interview questions
    3. **Practice & Learn**: Get AI-generated answers and practice your responses
    4. **Receive Feedback**: Get detailed evaluation and improvement suggestions
    5. **Track Progress**: Monitor your performance across different topics
    """)
    
    st.markdown("### ✨ Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **Intelligent Question Retrieval** using vector embeddings
        - **Personalized Answer Generation** based on job context
        - **Real-time Answer Evaluation** with detailed feedback
        - **Technical Term Explainer** for concepts you don't understand
        """)
    
    with col2:
        st.markdown("""
        - **Progress Tracking** with visual analytics
        - **Category-based Practice** (ML, System Design, Algorithms, etc.)
        - **STAR Method** guidance for behavioral questions
        - **Follow-up Questions** to prepare you thoroughly
        """)
    
    st.info("💡 **Tip**: Start by analyzing a real job description from your target company for the most relevant practice!")

# ========== JOB DESCRIPTION ANALYSIS ==========
elif page == "Job Description Analysis":
    st.markdown("<h1 class='main-header'>Job Description Analysis</h1>", unsafe_allow_html=True)
    
    st.write("Paste a job description below to extract key information and get relevant interview questions.")
    
    job_description = st.text_area(
        "Job Description",
        height=300,
        placeholder="Paste the full job description here..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if analyze_button and job_description:
        with st.spinner("Analyzing job description..."):
            try:
                # Analyze JD
                analysis = st.session_state.jd_analyzer.analyze(job_description)
                st.session_state.current_jd_analysis = analysis
                
                st.success("✅ Analysis complete!")
                
                # Display results
                st.markdown("### 📋 Analysis Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🎯 Job Role")
                    st.info(analysis.get('job_role', 'Not specified'))
                    
                    st.markdown("#### 📊 Experience Level")
                    st.info(analysis.get('experience_level', 'Not specified'))
                    
                    st.markdown("#### ✅ Required Skills")
                    for skill in analysis.get('required_skills', [])[:10]:
                        st.markdown(f"- {skill}")
                
                with col2:
                    st.markdown("#### 💻 Key Technologies")
                    for tech in analysis.get('technologies', [])[:10]:
                        st.markdown(f"- {tech}")
                    
                    st.markdown("#### 🎤 Interview Focus Areas")
                    for area in analysis.get('interview_focus_areas', [])[:5]:
                        st.markdown(f"- {area}")
                
                st.markdown("### 📝 Summary")
                st.write(analysis.get('summary', 'No summary available'))
                
                # Get relevant questions
                st.markdown("### 🎯 Retrieving Relevant Interview Questions...")
                
                with st.spinner("Searching question database..."):
                    search_query = st.session_state.jd_analyzer.generate_search_query(analysis)
                    questions = st.session_state.vector_store.search_questions(
                        query=search_query,
                        n_results=10
                    )
                    st.session_state.current_questions = questions
                    
                    st.success(f"✅ Found {len(questions)} relevant questions!")
                    
                    # Display questions
                    for i, q in enumerate(questions, 1):
                        with st.expander(f"Question {i}: {q['question'][:100]}..."):
                            st.markdown(f"**Full Question:** {q['question']}")
                            st.markdown(f"**Category:** {q['category']}")
                            st.markdown(f"**Difficulty:** {q['difficulty']}")
                            st.markdown(f"**Relevance Score:** {q['relevance_score']:.2f}")
                            
                            if st.button(f"Practice this question", key=f"practice_{i}"):
                                st.session_state.current_question_idx = i - 1
                                st.switch_page("pages/practice.py") if hasattr(st, 'switch_page') else st.info("Go to Practice Interview page")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
    
    elif analyze_button and not job_description:
        st.warning("⚠️ Please paste a job description first!")

# ========== PRACTICE INTERVIEW ==========
elif page == "Practice Interview":
    st.markdown("<h1 class='main-header'>Practice Interview</h1>", unsafe_allow_html=True)
    
    if not st.session_state.current_questions:
        st.warning("⚠️ No questions loaded. Please analyze a job description first!")
        st.info("Go to 'Job Description Analysis' page to get started.")
    else:
        # Question navigation
        total_questions = len(st.session_state.current_questions)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous") and st.session_state.current_question_idx > 0:
                st.session_state.current_question_idx -= 1
                st.rerun()
        with col2:
            st.markdown(f"<p style='text-align: center;'>Question {st.session_state.current_question_idx + 1} of {total_questions}</p>", unsafe_allow_html=True)
        with col3:
            if st.button("Next ➡️") and st.session_state.current_question_idx < total_questions - 1:
                st.session_state.current_question_idx += 1
                st.rerun()
        
        # Current question
        current_q = st.session_state.current_questions[st.session_state.current_question_idx]
        
        st.markdown("### 📝 Question")
        st.markdown(f"<div class='info-box'><h3>{current_q['question']}</h3></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", current_q['category'])
        col2.metric("Difficulty", current_q['difficulty'])
        col3.metric("Relevance", f"{current_q['relevance_score']:.2f}")
        
        # Tabs for different modes
        tab1, tab2, tab3 = st.tabs(["✍️ Your Answer", "🤖 AI-Generated Answer", "📊 Get Feedback"])
        
        with tab1:
            st.markdown("### Write Your Answer")
            user_answer = st.text_area(
                "Your answer:",
                height=250,
                placeholder="Type your answer here...",
                key="user_answer"
            )
            
            if st.button("💾 Save Answer", type="primary"):
                if user_answer:
                    st.success("✅ Answer saved! Go to 'Get Feedback' tab for evaluation.")
                    st.session_state.current_user_answer = user_answer
                else:
                    st.warning("⚠️ Please write an answer first!")
        
        with tab2:
            st.markdown("### AI-Generated Model Answer")
            st.info("Get a professionally crafted answer to learn from")
            
            col1, col2 = st.columns(2)
            with col1:
                use_star = st.checkbox("Use STAR method", value=current_q['category'] == 'Behavioral')
            
            if st.button("🤖 Generate Answer", type="primary"):
                with st.spinner("Generating answer..."):
                    try:
                        job_context = None
                        if st.session_state.current_jd_analysis:
                            job_context = st.session_state.current_jd_analysis.get('summary', '')
                        
                        answer = st.session_state.llm_service.generate_answer(
                            question=current_q['question'],
                            job_context=job_context,
                            answer_hints=current_q.get('answer_hints'),
                            use_star_method=use_star
                        )
                        
                        st.session_state.generated_answer = answer
                        
                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")
            
            if st.session_state.generated_answer:
                st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                st.markdown(st.session_state.generated_answer)
                st.markdown("</div>", unsafe_allow_html=True)
                
                if st.button("🔄 Generate Different Answer"):
                    st.session_state.generated_answer = ""
                    st.rerun()
        
        with tab3:
            st.markdown("### Get Detailed Feedback")
            
            if 'current_user_answer' not in st.session_state or not st.session_state.current_user_answer:
                st.info("💡 Write and save your answer in the 'Your Answer' tab first!")
            else:
                st.write("**Your Answer:**")
                st.write(st.session_state.current_user_answer)
                
                if st.button("📊 Evaluate My Answer", type="primary"):
                    with st.spinner("Evaluating your answer..."):
                        try:
                            evaluation = st.session_state.evaluator.evaluate_comprehensive(
                                question=current_q['question'],
                                user_answer=st.session_state.current_user_answer,
                                category=current_q['category'],
                                difficulty=current_q['difficulty'],
                                ideal_answer=st.session_state.generated_answer if st.session_state.generated_answer else None
                            )
                            
                            # Display scores
                            st.markdown("### 🎯 Evaluation Results")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Overall Score", f"{evaluation['overall_score']}/10")
                            col2.metric("Grade", evaluation['grade'])
                            col3.metric("Difficulty", current_q['difficulty'])
                            
                            # Detailed scores
                            st.markdown("### 📊 Detailed Breakdown")
                            cols = st.columns(5)
                            for i, (aspect, score) in enumerate(evaluation['detailed_scores'].items()):
                                cols[i].metric(aspect.replace('_', ' ').title(), f"{score}/10")
                            
                            # Strengths
                            st.markdown("### ✅ Strengths")
                            for strength in evaluation['strengths']:
                                st.success(f"✓ {strength}")
                            
                            # Areas for improvement
                            st.markdown("### 🎯 Areas for Improvement")
                            for weakness in evaluation['weaknesses']:
                                st.warning(f"⚠ {weakness}")
                            
                            # Improvement suggestions
                            st.markdown("### 💡 Specific Suggestions")
                            for i, suggestion in enumerate(evaluation['improvements'], 1):
                                st.info(f"{i}. {suggestion}")
                            
                            # Follow-up questions
                            st.markdown("### 🤔 Potential Follow-up Questions")
                            st.write("An interviewer might ask:")
                            for followup in evaluation['followup_questions']:
                                st.markdown(f"- {followup}")
                            
                            # Save to history
                            history_entry = {
                                "question": current_q['question'],
                                "category": current_q['category'],
                                "difficulty": current_q['difficulty'],
                                "user_answer": st.session_state.current_user_answer,
                                "score": evaluation['overall_score'],
                                "grade": evaluation['grade'],
                                "timestamp": datetime.now().isoformat()
                            }
                            st.session_state.practice_history.append(history_entry)
                            
                            st.success("✅ Evaluation complete! Results saved to your progress.")
                            
                        except Exception as e:
                            st.error(f"❌ Error during evaluation: {str(e)}")

# ========== PROGRESS DASHBOARD ==========
elif page == "Progress Dashboard":
    st.markdown("<h1 class='main-header'>Progress Dashboard</h1>", unsafe_allow_html=True)
    
    if not st.session_state.practice_history:
        st.info("📝 No practice history yet. Start practicing to see your progress!")
    else:
        # Overall statistics
        st.markdown("### 📈 Overall Statistics")
        
        total_questions = len(st.session_state.practice_history)
        avg_score = sum(h['score'] for h in st.session_state.practice_history) / total_questions
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Questions Practiced", total_questions)
        col2.metric("Average Score", f"{avg_score:.1f}/10")
        col3.metric("Average Grade", "B+" if avg_score >= 8 else "B" if avg_score >= 7 else "C+")
        
        # Calculate improvement trend
        if total_questions >= 4:
            first_half = st.session_state.practice_history[:total_questions//2]
            second_half = st.session_state.practice_history[total_questions//2:]
            first_avg = sum(h['score'] for h in first_half) / len(first_half)
            second_avg = sum(h['score'] for h in second_half) / len(second_half)
            improvement = second_avg - first_avg
            col4.metric("Improvement", f"{improvement:+.1f}", delta=f"{improvement:+.1f}")
        
        # Score history chart
        st.markdown("### 📊 Score History")
        scores = [h['score'] for h in st.session_state.practice_history]
        st.line_chart(scores)
        
        # Category breakdown
        st.markdown("### 📚 Performance by Category")
        
        category_stats = {}
        for h in st.session_state.practice_history:
            cat = h['category']
            if cat not in category_stats:
                category_stats[cat] = {'count': 0, 'total_score': 0}
            category_stats[cat]['count'] += 1
            category_stats[cat]['total_score'] += h['score']
        
        for cat, stats in category_stats.items():
            avg = stats['total_score'] / stats['count']
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(f"**{cat}**")
            col2.write(f"Questions: {stats['count']}")
            col3.write(f"Avg Score: {avg:.1f}/10")
            st.progress(avg / 10)
        
        # Recent practice history
        st.markdown("### 📝 Recent Practice History")
        for i, h in enumerate(reversed(st.session_state.practice_history[-5:]), 1):
            with st.expander(f"{h['question'][:80]}... - Score: {h['score']}/10 ({h['grade']})"):
                st.markdown(f"**Category:** {h['category']}")
                st.markdown(f"**Difficulty:** {h['difficulty']}")
                st.markdown(f"**Your Answer:**")
                st.write(h['user_answer'])
                st.markdown(f"**Score:** {h['score']}/10 (Grade: {h['grade']})")

# ========== TERM EXPLAINER ==========
elif page == "Term Explainer":
    st.markdown("<h1 class='main-header'>Technical Term Explainer</h1>", unsafe_allow_html=True)
    
    st.write("Don't understand a technical term? Get a clear, simple explanation!")
    
    term = st.text_input("Enter a technical term:", placeholder="e.g., stateless, microservices, batch normalization")
    
    context = st.text_area(
        "Context (optional):",
        height=100,
        placeholder="Provide additional context if needed..."
    )
    
    if st.button("🔍 Explain", type="primary"):
        if term:
            with st.spinner(f"Explaining '{term}'..."):
                try:
                    explanation = st.session_state.llm_service.explain_term(term, context if context else None)
                    
                    st.markdown("### 💡 Explanation")
                    st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                    st.markdown(explanation)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error generating explanation: {str(e)}")
        else:
            st.warning("⚠️ Please enter a term to explain!")

# ========== ABOUT ==========
elif page == "About":
    st.markdown("<h1 class='main-header'>About AI Interview Assistant</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### Project Overview
    
    The **AI Interview Assistant** is an intelligent tool that leverages **Retrieval-Augmented Generation (RAG)** 
    and **Large Language Models (LLMs)** to help candidates prepare for technical interviews.
    
    ### 🏗️ Architecture
    
    **Key Components:**
    
    1. **Vector Database (ChromaDB)**: Stores interview questions as embeddings for semantic search
    2. **Job Description Analyzer**: Extracts skills and requirements using LLM
    3. **RAG Pipeline**: Retrieves relevant questions based on job requirements
    4. **LLM Service**: Generates personalized answers and feedback using GPT-4
    5. **Answer Evaluator**: Provides detailed scoring and improvement suggestions
    6. **Progress Tracker**: Monitors improvement over time
    
    ### 🛠️ Tech Stack
    
    - **Backend**: Python 3.8+
    - **LLM**: OpenAI GPT-4
    - **Vector DB**: ChromaDB with OpenAI embeddings
    - **Frontend**: Streamlit
    - **Additional**: sentence-transformers, pandas, numpy
    
    ### ✨ Features
    
    - 📄 Smart job description analysis
    - 🎯 RAG-powered question retrieval
    - 🤖 AI-generated model answers
    - 📊 Detailed answer evaluation
    - 💡 Technical term explainer
    - 📈 Progress tracking and analytics
    - 🎤 STAR method for behavioral questions
    
    ### 📚 Question Database
    
    - **150+ curated questions** across 11 categories
    - Categories: Python, DSA, System Design, ML, DL, NLP, SQL, Cloud, DevOps, Behavioral, General SE
    - Difficulty levels: Easy, Medium, Hard
    - Metadata: keywords, hints, relevance scoring
    
    ### 🚀 Why This Project Stands Out
    
    1. **RAG Implementation**: Demonstrates understanding of modern AI architecture
    2. **End-to-End Solution**: Complete product from data to UI
    3. **Practical Application**: Solves a real problem for job seekers
    4. **ML Engineering**: Includes evaluation, metrics, and tracking
    5. **Resume-Worthy**: Shows expertise in LLMs, embeddings, and vector databases
    
    ### 👨‍💻 Developer
    
    Built as a portfolio project demonstrating:
    - RAG architecture implementation
    - LLM integration and prompt engineering
    - Vector database management
    - Full-stack AI application development
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: November 2025
    """)
    
    st.info("💡 **Tip**: This project demonstrates key AI engineering concepts that are highly valued in the industry!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 System Status")
if st.session_state.vector_store:
    stats = st.session_state.vector_store.get_stats()
    st.sidebar.success(f"✅ {stats['total_questions']} questions loaded")
st.sidebar.info(f"🎯 {len(st.session_state.practice_history)} questions practiced")
