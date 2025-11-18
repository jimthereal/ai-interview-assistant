import axios from 'axios';
import type {
  JobDescriptionResponse,
  Question,
  EvaluationResponse,
  ProgressResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Job Description Analysis
export const analyzeJobDescription = async (jobDescription: string): Promise<JobDescriptionResponse> => {
  const response = await api.post('/api/analyze-jd', { job_description: jobDescription });
  return response.data;
};

// Questions
export const getQuestions = async (params?: {
  category?: string;
  difficulty?: string;
  search?: string;
  limit?: number;
}): Promise<{ questions: Question[]; total: number }> => {
  const response = await api.get('/api/questions', { params });
  return response.data;
};

export const getCategories = async (): Promise<{ categories: string[] }> => {
  const response = await api.get('/api/categories');
  return response.data;
};

// Answers
export const generateAnswer = async (data: {
  question: string;
  category: string;
  difficulty: string;
  job_context?: string;
  hints?: string[];
}): Promise<{ answer: string; formatted: boolean }> => {
  const response = await api.post('/api/generate-answer', data);
  return response.data;
};

export const evaluateAnswer = async (data: {
  question: string;
  user_answer: string;
  category: string;
  difficulty: string;
  model_answer?: string;
}): Promise<EvaluationResponse> => {
  const response = await api.post('/api/evaluate-answer', data);
  return response.data;
};

// Progress
export const getProgress = async (): Promise<ProgressResponse> => {
  const response = await api.get('/api/progress');
  return response.data;
};

// Term Explainer
export const explainTerm = async (term: string, context?: string): Promise<{
  term: string;
  explanation: string;
  examples: string[];
}> => {
  const response = await api.post('/api/explain-term', null, {
    params: { term, context },
  });
  return response.data;
};

export default api;
