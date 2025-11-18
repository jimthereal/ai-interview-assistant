import { create } from 'zustand';
import type { Question, JobDescriptionResponse, EvaluationResponse } from '../types';

interface AppState {
  // Job Analysis
  currentJobAnalysis: JobDescriptionResponse | null;
  setJobAnalysis: (analysis: JobDescriptionResponse | null) => void;

  // Current Question
  currentQuestion: Question | null;
  setCurrentQuestion: (question: Question | null) => void;

  // Current Answer & Evaluation
  currentAnswer: string;
  setCurrentAnswer: (answer: string) => void;
  modelAnswer: string | null;
  setModelAnswer: (answer: string | null) => void;
  evaluation: EvaluationResponse | null;
  setEvaluation: (evaluation: EvaluationResponse | null) => void;

  // UI State
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  
  // Reset functions
  resetQuestion: () => void;
  resetAll: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Job Analysis
  currentJobAnalysis: null,
  setJobAnalysis: (analysis) => set({ currentJobAnalysis: analysis }),

  // Current Question
  currentQuestion: null,
  setCurrentQuestion: (question) => set({ currentQuestion: question }),

  // Answers & Evaluation
  currentAnswer: '',
  setCurrentAnswer: (answer) => set({ currentAnswer: answer }),
  modelAnswer: null,
  setModelAnswer: (answer) => set({ modelAnswer: answer }),
  evaluation: null,
  setEvaluation: (evaluation) => set({ evaluation: evaluation }),

  // UI State
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),

  // Reset functions
  resetQuestion: () =>
    set({
      currentQuestion: null,
      currentAnswer: '',
      modelAnswer: null,
      evaluation: null,
    }),
  
  resetAll: () =>
    set({
      currentJobAnalysis: null,
      currentQuestion: null,
      currentAnswer: '',
      modelAnswer: null,
      evaluation: null,
      isLoading: false,
    }),
}));
