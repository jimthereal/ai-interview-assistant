import { create } from 'zustand';

export interface ExplanationResult {
    definition: string;
    analogy: string;
    key_points: string[];
    example: string;
    why_it_matters: string;
}

interface ExplainerState {
    term: string;
    result: ExplanationResult | null;
    isLoading: boolean;
    error: string | null;
    setTerm: (term: string) => void;
    setResult: (result: ExplanationResult | null) => void;
    setIsLoading: (isLoading: boolean) => void;
    setError: (error: string | null) => void;
}

export const useExplainerStore = create<ExplainerState>()((set) => ({
    term: '',
    result: null,
    isLoading: false,
    error: null,
    setTerm: (term) => set({ term }),
    setResult: (result) => set({ result }),
    setIsLoading: (isLoading) => set({ isLoading }),
    setError: (error) => set({ error }),
}));
