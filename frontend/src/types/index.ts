export interface Question {
  id: string;
  question: string;
  category: string;
  difficulty: string;
  hints?: string[];
}

export interface JobAnalysis {
  required_skills: string[];
  preferred_skills: string[];
  experience_level: string;
  job_role: string;
}

export interface JobDescriptionResponse {
  analysis: JobAnalysis;
  summary: string;
  matched_questions: Question[];
}

export interface AnswerScores {
  overall: number;
  clarity: number;
  completeness: number;
  accuracy: number;
  professionalism: number;
}

export interface EvaluationResponse {
  scores: AnswerScores;
  strengths: string[];
  improvements: string[];
  follow_up_questions: string[];
  feedback: string;
}

export interface PracticeEntry {
  question_id: string;
  question: string;
  category: string;
  score: number;
  timestamp: string;
}

export interface ProgressStats {
  total_questions_practiced: number;
  average_score: number;
  category_breakdown: {
    [category: string]: {
      count: number;
      average_score: number;
    };
  };
  recent_practices: PracticeEntry[];
}

export interface ProgressResponse {
  stats: ProgressStats;
  improvement_suggestions: string[];
}
