"""
LLM Service Module
Handles interactions with Groq API for LLM operations
"""
from typing import Dict, List, Optional
from config.config import Config
from groq import Groq


class LLMService:
    """Service for LLM-based answer generation and analysis using Groq"""
    
    def __init__(self):
        """Initialize LLM service with Groq"""
        self.model = Config.LLM_MODEL
        self.temperature = Config.TEMPERATURE
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def _call_llm(self, messages: List[Dict], max_tokens: int = None) -> str:
        """Call Groq API"""
        if max_tokens is None:
            max_tokens = Config.ANSWER_MAX_TOKENS
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error calling Groq API: {str(e)}")
    
    def generate_answer(
        self,
        question: str,
        job_context: Optional[str] = None,
        user_experience: Optional[str] = None,
        answer_hints: Optional[str] = None,
        use_star_method: bool = False
    ) -> str:
        """
        Generate a personalized answer to an interview question
        
        Args:
            question: The interview question
            job_context: Context from the job description
            user_experience: User's experience level or background
            answer_hints: Hints for answering
            use_star_method: Use STAR method for behavioral questions
            
        Returns:
            Generated answer
        """
        # Build context
        context_parts = []
        
        if job_context:
            context_parts.append(f"Job Context: {job_context}")
        
        if user_experience:
            context_parts.append(f"Candidate Background: {user_experience}")
        
        if answer_hints:
            context_parts.append(f"Key Points to Cover: {answer_hints}")
        
        context = "\n".join(context_parts) if context_parts else "No specific context provided."
        
        # Build prompt
        if use_star_method:
            prompt = f"""You are an expert interview coach. Generate a strong answer to this behavioral interview question using the STAR method (Situation, Task, Action, Result).

Interview Question: {question}

{context}

Provide a compelling answer that:
1. Follows the STAR framework
2. Is specific and detailed
3. Demonstrates relevant skills and achievements
4. Is concise (2-3 minutes when spoken)
5. Sounds natural and conversational

Answer:"""
        else:
            prompt = f"""You are an expert interview coach. Generate a strong, professional answer to this technical interview question.

Interview Question: {question}

{context}

Provide a clear, comprehensive answer that:
1. Directly addresses the question
2. Demonstrates deep understanding
3. Includes relevant examples or use cases
4. Is well-structured and easy to follow
5. Shows enthusiasm and expertise
6. Is concise but complete (2-3 minutes when spoken)

Answer:"""
        
        # Generate answer
        response = self._call_llm(
            messages=[
                {"role": "system", "content": "You are an expert interview coach helping candidates prepare for technical interviews."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=Config.ANSWER_MAX_TOKENS
        )
        
        return response
    
    def explain_term(self, term: str, context: Optional[str] = None) -> str:
        """
        Explain a technical term in simple language
        
        Args:
            term: Technical term to explain
            context: Additional context
            
        Returns:
            Simple explanation
        """
        prompt = f"""Explain the technical term "{term}" in simple, clear language that a beginner can understand.

{f"Context: {context}" if context else ""}

Provide:
1. A simple definition (1-2 sentences)
2. Why it matters
3. A real-world example or analogy
4. Common use cases

Keep it concise and accessible."""

        response = self._call_llm(
            messages=[
                {"role": "system", "content": "You are a patient teacher who excels at explaining complex technical concepts in simple terms."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        
        return response
    
    def evaluate_answer(
        self,
        question: str,
        user_answer: str,
        ideal_answer: Optional[str] = None
    ) -> Dict:
        """
        Evaluate a user's answer and provide feedback
        
        Args:
            question: The interview question
            user_answer: User's answer
            ideal_answer: Optional ideal answer for comparison
            
        Returns:
            Dictionary with score and feedback
        """
        prompt = f"""You are an expert interview coach. Evaluate this candidate's answer to an interview question.

Question: {question}

Candidate's Answer: {user_answer}

{f"Reference Answer: {ideal_answer}" if ideal_answer else ""}

Provide evaluation in this format:

SCORE: [0-10]

STRENGTHS:
- [List 2-3 strong points]

AREAS FOR IMPROVEMENT:
- [List 2-3 specific improvements]

SUGGESTIONS:
- [2-3 actionable tips to enhance the answer]

Be constructive, specific, and encouraging."""

        response = self._call_llm(
            messages=[
                {"role": "system", "content": "You are an expert interview coach providing constructive feedback."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        feedback = response
        
        # Parse score
        score = 7  # Default
        if "SCORE:" in feedback:
            try:
                score_line = [line for line in feedback.split("\n") if "SCORE:" in line][0]
                score = int(score_line.split("[")[1].split("-")[0])
            except:
                pass
        
        return {
            "score": score,
            "feedback": feedback
        }
    
    def suggest_improvements(self, answer: str, question: str) -> List[str]:
        """
        Suggest specific improvements for an answer
        
        Args:
            answer: The answer to improve
            question: The original question
            
        Returns:
            List of improvement suggestions
        """
        prompt = f"""Review this interview answer and suggest 3-4 specific, actionable improvements.

Question: {question}

Answer: {answer}

Provide numbered, specific suggestions that would make this answer stronger. Focus on:
- Content gaps
- Structure improvements
- Clarity enhancements
- Impact amplification"""

        response = self._call_llm(
            messages=[
                {"role": "system", "content": "You are an expert interview coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        
        suggestions_text = response
        
        # Parse into list
        suggestions = []
        for line in suggestions_text.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-") or line.startswith("•")):
                # Remove numbering/bullets
                clean_line = line.lstrip("0123456789.-•) ").strip()
                if clean_line:
                    suggestions.append(clean_line)
        
        return suggestions[:4]  # Return max 4 suggestions
    
    def generate_followup_questions(self, question: str, answer: str) -> List[str]:
        """
        Generate potential follow-up questions an interviewer might ask
        
        Args:
            question: Original question
            answer: Candidate's answer
            
        Returns:
            List of follow-up questions
        """
        prompt = f"""Based on this interview exchange, generate 3 likely follow-up questions an interviewer might ask.

Question: {question}

Answer: {answer}

Generate follow-up questions that:
1. Probe deeper into the answer
2. Test understanding
3. Are realistic for an actual interview

List 3 questions, one per line."""

        response = self._call_llm(
            messages=[
                {"role": "system", "content": "You are an experienced technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        followups_text = response
        
        # Parse into list
        followups = []
        for line in followups_text.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-") or line.endswith("?")):
                clean_line = line.lstrip("0123456789.-•) ").strip()
                if clean_line:
                    followups.append(clean_line)
        
        return followups[:3]
