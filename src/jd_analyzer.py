"""
Job Description Analyzer
Extracts skills, technologies, and requirements from job descriptions using LLM
"""
import re
from typing import Dict, List, Set
from config.config import Config


class JDAnalyzer:
    """Analyzes job descriptions to extract relevant information"""
    
    def __init__(self):
        """Initialize JD Analyzer"""
        # Import and initialize LLM service
        from src.llm_service import LLMService
        self.llm_service = LLMService()
        
        # Common technology keywords
        self.tech_keywords = {
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
            "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi",
            "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git",
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "rest", "graphql", "microservices", "api", "ci/cd",
            "machine learning", "deep learning", "nlp", "computer vision",
            "agile", "scrum", "devops"
        }
    
    def analyze(self, job_description: str) -> Dict:
        """
        Analyze job description comprehensively
        
        Args:
            job_description: The job description text
            
        Returns:
            Dictionary with extracted information
        """
        # Extract basic info
        extracted_skills = self._extract_skills_simple(job_description)
        
        # Use LLM for comprehensive analysis
        llm_analysis = self._analyze_with_llm(job_description)
        
        # Combine results
        result = {
            "raw_text": job_description,
            "extracted_skills": list(extracted_skills),
            "required_skills": llm_analysis.get("required_skills", []),
            "preferred_skills": llm_analysis.get("preferred_skills", []),
            "experience_level": llm_analysis.get("experience_level", "Mid-level"),
            "job_role": llm_analysis.get("job_role", "Not specified"),
            "key_responsibilities": llm_analysis.get("key_responsibilities", []),
            "technologies": llm_analysis.get("technologies", []),
            "soft_skills": llm_analysis.get("soft_skills", []),
            "interview_focus_areas": llm_analysis.get("interview_focus_areas", []),
            "summary": llm_analysis.get("summary", "")
        }
        
        return result
    
    def _extract_skills_simple(self, text: str) -> Set[str]:
        """Extract skills using keyword matching"""
        text_lower = text.lower()
        found_skills = set()
        
        for keyword in self.tech_keywords:
            # Look for whole word matches
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(keyword)
        
        return found_skills
    
    def _analyze_with_llm(self, job_description: str) -> Dict:
        """Use LLM for comprehensive job description analysis"""
        prompt = f"""Analyze this job description and extract key information for interview preparation.

Job Description:
{job_description}

Provide a structured analysis in the following format:

JOB ROLE: [Title/Role]

EXPERIENCE LEVEL: [Entry/Mid-level/Senior/Lead]

REQUIRED SKILLS:
- [Skill 1]
- [Skill 2]
- [Skill 3]

PREFERRED SKILLS:
- [Skill 1]
- [Skill 2]

KEY TECHNOLOGIES:
- [Technology 1]
- [Technology 2]
- [Technology 3]

KEY RESPONSIBILITIES:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

SOFT SKILLS:
- [Soft skill 1]
- [Soft skill 2]

INTERVIEW FOCUS AREAS:
- [Area 1]
- [Area 2]
- [Area 3]

SUMMARY:
[2-3 sentence summary of the role and ideal candidate]

Be specific and extract actual skills/technologies mentioned."""

        try:
            response = self.llm_service._call_llm(
                messages=[
                    {"role": "system", "content": "You are an expert recruiter and job description analyzer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )
            
            return self._parse_llm_analysis(response)
            
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            return {}
    
    def _parse_llm_analysis(self, analysis_text: str) -> Dict:
        """Parse structured analysis from LLM output"""
        result = {
            "required_skills": [],
            "preferred_skills": [],
            "experience_level": "Mid-level",
            "job_role": "Not specified",
            "key_responsibilities": [],
            "technologies": [],
            "soft_skills": [],
            "interview_focus_areas": [],
            "summary": ""
        }
        
        current_section = None
        
        for line in analysis_text.split("\n"):
            line = line.strip()
            
            if not line:
                continue
            
            # Identify sections
            if "JOB ROLE:" in line:
                result["job_role"] = line.split("JOB ROLE:")[-1].strip()
            elif "EXPERIENCE LEVEL:" in line:
                result["experience_level"] = line.split("EXPERIENCE LEVEL:")[-1].strip()
            elif "REQUIRED SKILLS:" in line:
                current_section = "required_skills"
            elif "PREFERRED SKILLS:" in line:
                current_section = "preferred_skills"
            elif "KEY TECHNOLOGIES:" in line:
                current_section = "technologies"
            elif "KEY RESPONSIBILITIES:" in line:
                current_section = "key_responsibilities"
            elif "SOFT SKILLS:" in line:
                current_section = "soft_skills"
            elif "INTERVIEW FOCUS AREAS:" in line:
                current_section = "interview_focus_areas"
            elif "SUMMARY:" in line:
                current_section = "summary"
                result["summary"] = line.split("SUMMARY:")[-1].strip()
            elif line.startswith("-") or line.startswith("•"):
                # Extract list item
                item = line.lstrip("-•").strip()
                if item and current_section and current_section != "summary":
                    result[current_section].append(item)
            elif current_section == "summary" and line:
                # Continue summary
                result["summary"] += " " + line
        
        return result
    
    def generate_search_query(self, analysis: Dict) -> str:
        """
        Generate optimized search query for vector store
        
        Args:
            analysis: Job description analysis
            
        Returns:
            Search query string
        """
        query_parts = []
        
        # Add job role
        if analysis.get("job_role"):
            query_parts.append(analysis["job_role"])
        
        # Add top required skills
        if analysis.get("required_skills"):
            query_parts.extend(analysis["required_skills"][:5])
        
        # Add key technologies
        if analysis.get("technologies"):
            query_parts.extend(analysis["technologies"][:5])
        
        # Add interview focus areas
        if analysis.get("interview_focus_areas"):
            query_parts.extend(analysis["interview_focus_areas"][:3])
        
        return " ".join(query_parts)
    
    def categorize_questions_needed(self, analysis: Dict) -> List[str]:
        """
        Determine which question categories are most relevant
        
        Args:
            analysis: Job description analysis
            
        Returns:
            List of relevant question categories
        """
        categories = []
        
        all_skills = (
            analysis.get("required_skills", []) + 
            analysis.get("technologies", []) +
            analysis.get("interview_focus_areas", [])
        )
        
        all_skills_lower = [s.lower() for s in all_skills]
        
        # Map skills to categories
        if any(term in all_skills_lower for term in ["python", "java", "javascript", "c++"]):
            categories.append("Python")  # or specific language
        
        if any(term in all_skills_lower for term in ["algorithm", "data structure", "leetcode", "coding"]):
            categories.append("Data Structures & Algorithms")
        
        if any(term in all_skills_lower for term in ["system design", "architecture", "scalability", "distributed"]):
            categories.append("System Design")
        
        if any(term in all_skills_lower for term in ["machine learning", "ml", "ai", "model"]):
            categories.append("Machine Learning")
        
        if any(term in all_skills_lower for term in ["deep learning", "neural network", "tensorflow", "pytorch"]):
            categories.append("Deep Learning")
        
        if any(term in all_skills_lower for term in ["nlp", "natural language", "text", "language model"]):
            categories.append("NLP")
        
        if any(term in all_skills_lower for term in ["sql", "database", "postgresql", "mysql", "mongodb"]):
            categories.append("SQL & Databases")
        
        if any(term in all_skills_lower for term in ["aws", "azure", "gcp", "cloud"]):
            categories.append("Cloud Computing")
        
        if any(term in all_skills_lower for term in ["docker", "kubernetes", "ci/cd", "devops"]):
            categories.append("DevOps")
        
        # Always include behavioral
        categories.append("Behavioral")
        
        # Default to general if nothing specific
        if not categories:
            categories.append("General Software Engineering")
        
        return list(set(categories))
    
    def explain_term(self, term: str, context: str = None) -> str:
        """
        Explain a technical term in simple language
        
        Args:
            term: The technical term to explain
            context: Optional context for more specific explanation
            
        Returns:
            String explanation of the term
        """
        # Use the LLMService's explain_term method
        return self.llm_service.explain_term(term, context)
