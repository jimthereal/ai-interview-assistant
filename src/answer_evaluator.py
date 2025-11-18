"""
Answer Evaluator Module
Evaluates user answers and provides structured feedback
"""
from typing import Dict, List
from src.llm_service import LLMService


class AnswerEvaluator:
    """Evaluates and scores interview answers"""
    
    def __init__(self):
        """Initialize the evaluator with LLM service"""
        self.llm_service = LLMService()
    
    def evaluate_comprehensive(
        self,
        question: str,
        user_answer: str,
        category: str,
        difficulty: str,
        ideal_answer: str = None
    ) -> Dict:
        """
        Comprehensive evaluation of an answer
        
        Args:
            question: The interview question
            user_answer: User's answer
            category: Question category
            difficulty: Question difficulty
            ideal_answer: Optional reference answer
            
        Returns:
            Dictionary with detailed evaluation
        """
        # Get basic evaluation from LLM
        evaluation = self.llm_service.evaluate_answer(
            question=question,
            user_answer=user_answer,
            ideal_answer=ideal_answer
        )
        
        # Calculate detailed scores
        detailed_scores = self._calculate_detailed_scores(
            question, user_answer, category, difficulty
        )
        
        # Get improvement suggestions
        improvements = self.llm_service.suggest_improvements(user_answer, question)
        
        # Generate follow-up questions
        followups = self.llm_service.generate_followup_questions(question, user_answer)
        
        return {
            "overall_score": evaluation["score"],
            "detailed_scores": detailed_scores,
            "feedback": evaluation["feedback"],
            "improvements": improvements,
            "followup_questions": followups,
            "strengths": self._extract_strengths(evaluation["feedback"]),
            "weaknesses": self._extract_weaknesses(evaluation["feedback"]),
            "grade": self._score_to_grade(evaluation["score"]),
            "category": category,
            "difficulty": difficulty
        }
    
    def _calculate_detailed_scores(
        self, question: str, answer: str, category: str, difficulty: str
    ) -> Dict[str, int]:
        """Calculate detailed component scores"""
        # Simple heuristics (can be made more sophisticated)
        word_count = len(answer.split())
        
        # Clarity score (based on answer length and structure)
        if word_count < 20:
            clarity = 4
        elif word_count < 50:
            clarity = 6
        elif word_count < 150:
            clarity = 8
        else:
            clarity = 7  # Too long might be less clear
        
        # Completeness (simple heuristic based on length)
        if word_count < 30:
            completeness = 5
        elif word_count < 100:
            completeness = 7
        else:
            completeness = 9
        
        # Technical accuracy (would need LLM for real assessment)
        technical_accuracy = 7  # Placeholder
        
        # Structure (check for paragraphs, bullet points, etc.)
        has_structure = '\n' in answer or '.' in answer
        structure = 8 if has_structure else 6
        
        # Relevance (keyword-based simple check)
        question_keywords = set(question.lower().split())
        answer_keywords = set(answer.lower().split())
        overlap = len(question_keywords & answer_keywords)
        relevance = min(10, 5 + overlap)
        
        return {
            "clarity": clarity,
            "completeness": completeness,
            "technical_accuracy": technical_accuracy,
            "structure": structure,
            "relevance": relevance
        }
    
    def _extract_strengths(self, feedback: str) -> List[str]:
        """Extract strengths from feedback text"""
        strengths = []
        
        if "STRENGTHS:" in feedback:
            lines = feedback.split("STRENGTHS:")[1].split("AREAS FOR IMPROVEMENT:")[0]
            for line in lines.split("\n"):
                line = line.strip()
                if line and line.startswith("-"):
                    strengths.append(line[1:].strip())
        
        return strengths if strengths else ["Good attempt at answering the question"]
    
    def _extract_weaknesses(self, feedback: str) -> List[str]:
        """Extract weaknesses from feedback text"""
        weaknesses = []
        
        if "AREAS FOR IMPROVEMENT:" in feedback:
            lines = feedback.split("AREAS FOR IMPROVEMENT:")[1].split("SUGGESTIONS:")[0]
            for line in lines.split("\n"):
                line = line.strip()
                if line and line.startswith("-"):
                    weaknesses.append(line[1:].strip())
        
        return weaknesses if weaknesses else ["Could provide more specific examples"]
    
    def _score_to_grade(self, score: int) -> str:
        """Convert numerical score to letter grade"""
        if score >= 9:
            return "A"
        elif score >= 8:
            return "B+"
        elif score >= 7:
            return "B"
        elif score >= 6:
            return "C+"
        elif score >= 5:
            return "C"
        else:
            return "D"
    
    def quick_score(self, question: str, user_answer: str) -> int:
        """
        Quick scoring without detailed evaluation
        
        Args:
            question: The interview question
            user_answer: User's answer
            
        Returns:
            Score from 0-10
        """
        evaluation = self.llm_service.evaluate_answer(question, user_answer)
        return evaluation["score"]
    
    def compare_answers(
        self, 
        question: str, 
        answer1: str, 
        answer2: str
    ) -> Dict:
        """
        Compare two answers to the same question
        
        Args:
            question: The interview question
            answer1: First answer
            answer2: Second answer
            
        Returns:
            Comparison results
        """
        score1 = self.quick_score(question, answer1)
        score2 = self.quick_score(question, answer2)
        
        return {
            "answer1_score": score1,
            "answer2_score": score2,
            "better_answer": "Answer 1" if score1 > score2 else "Answer 2" if score2 > score1 else "Tie",
            "score_difference": abs(score1 - score2)
        }


class ProgressTracker:
    """Tracks user progress across sessions"""
    
    def __init__(self):
        """Initialize progress tracker"""
        self.sessions = []
    
    def add_session_data(self, session_data: Dict):
        """Add data from a practice session"""
        self.sessions.append(session_data)
    
    def get_statistics(self) -> Dict:
        """Calculate overall statistics"""
        if not self.sessions:
            return {
                "total_questions": 0,
                "average_score": 0,
                "categories_practiced": [],
                "improvement_trend": "N/A"
            }
        
        total_questions = sum(len(s.get("questions", [])) for s in self.sessions)
        all_scores = []
        categories = set()
        
        for session in self.sessions:
            for q_data in session.get("questions", []):
                if "score" in q_data:
                    all_scores.append(q_data["score"])
                if "category" in q_data:
                    categories.add(q_data["category"])
        
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
        
        # Calculate improvement trend (compare first half vs second half)
        trend = "N/A"
        if len(all_scores) >= 4:
            first_half_avg = sum(all_scores[:len(all_scores)//2]) / (len(all_scores)//2)
            second_half_avg = sum(all_scores[len(all_scores)//2:]) / (len(all_scores) - len(all_scores)//2)
            
            if second_half_avg > first_half_avg + 0.5:
                trend = "Improving ↗"
            elif second_half_avg < first_half_avg - 0.5:
                trend = "Declining ↘"
            else:
                trend = "Stable →"
        
        return {
            "total_questions": total_questions,
            "average_score": round(avg_score, 1),
            "categories_practiced": list(categories),
            "improvement_trend": trend,
            "total_sessions": len(self.sessions),
            "scores_history": all_scores
        }
    
    def get_category_breakdown(self) -> Dict[str, Dict]:
        """Get statistics breakdown by category"""
        category_data = {}
        
        for session in self.sessions:
            for q_data in session.get("questions", []):
                category = q_data.get("category", "Unknown")
                score = q_data.get("score", 0)
                
                if category not in category_data:
                    category_data[category] = {
                        "count": 0,
                        "total_score": 0,
                        "scores": []
                    }
                
                category_data[category]["count"] += 1
                category_data[category]["total_score"] += score
                category_data[category]["scores"].append(score)
        
        # Calculate averages
        for category, data in category_data.items():
            data["average_score"] = round(data["total_score"] / data["count"], 1)
        
        return category_data
    
    def get_recommendations(self) -> List[str]:
        """Get personalized recommendations based on progress"""
        recommendations = []
        
        stats = self.get_statistics()
        category_breakdown = self.get_category_breakdown()
        
        if stats["total_questions"] == 0:
            recommendations.append("Start practicing! Upload a job description to get personalized questions.")
            return recommendations
        
        # Find weak categories
        weak_categories = []
        for category, data in category_breakdown.items():
            if data["average_score"] < 6:
                weak_categories.append(category)
        
        if weak_categories:
            recommendations.append(
                f"Focus on improving: {', '.join(weak_categories[:3])}"
            )
        
        # Check overall performance
        if stats["average_score"] < 6:
            recommendations.append(
                "Practice more! Try explaining concepts out loud before writing."
            )
        elif stats["average_score"] > 8:
            recommendations.append(
                "Great job! Try tackling harder questions or new categories."
            )
        
        # Session frequency
        if len(self.sessions) < 3:
            recommendations.append(
                "Consistency is key! Try to practice regularly for best results."
            )
        
        return recommendations
