import { useState, useEffect } from 'react';
import { getQuestions, getCategories, generateAnswer, evaluateAnswer } from '../api/client';
import Loading from '../components/Loading';
import ScoreRing from '../components/ScoreRing';
import type { Question, EvaluationResponse, ModelAnswer } from '../types';

export default function Practice() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [modelAnswer, setModelAnswer] = useState<ModelAnswer | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingState, setLoadingState] = useState<'questions' | 'answer' | 'evaluation' | null>(null);

  const currentQuestion = questions[currentIndex];

  useEffect(() => {
    loadCategories();
    loadQuestions();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data.categories);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const loadQuestions = async (category?: string) => {
    setIsLoading(true);
    setLoadingState('questions');
    try {
      const data = await getQuestions({
        category: category || undefined,
        limit: 50,
      });
      setQuestions(data.questions);
      setCurrentIndex(0);
      resetAnswers();
    } catch (error) {
      console.error('Failed to load questions:', error);
    } finally {
      setIsLoading(false);
      setLoadingState(null);
    }
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    loadQuestions(category || undefined);
  };

  const resetAnswers = () => {
    setUserAnswer('');
    setModelAnswer(null);
    setEvaluation(null);
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      resetAnswers();
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      resetAnswers();
    }
  };

  const handleGenerateAnswer = async () => {
    if (!currentQuestion) return;

    setIsLoading(true);
    setLoadingState('answer');
    try {
      const result = await generateAnswer({
        question: currentQuestion.question,
        category: currentQuestion.category,
        difficulty: currentQuestion.difficulty,
        hints: currentQuestion.hints,
      });
      setModelAnswer(result.answer);
    } catch (error) {
      console.error('Failed to generate answer:', error);
    } finally {
      setIsLoading(false);
      setLoadingState(null);
    }
  };

  const handleEvaluate = async () => {
    if (!currentQuestion || !userAnswer.trim()) return;

    setIsLoading(true);
    setLoadingState('evaluation');
    try {
      const result = await evaluateAnswer({
        question: currentQuestion.question,
        user_answer: userAnswer,
        category: currentQuestion.category,
        difficulty: currentQuestion.difficulty,
        model_answer: modelAnswer?.detailed_answer || undefined,
      });
      setEvaluation(result);
    } catch (error) {
      console.error('Failed to evaluate answer:', error);
    } finally {
      setIsLoading(false);
      setLoadingState(null);
    }
  };

  if (!currentQuestion && !isLoading) {
    return (
      <div className="text-center py-12">
        <p className="text-[var(--text-secondary)]">No questions available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold">Practice Interview Questions</h1>
          <p className="text-[var(--text-secondary)] mt-1">
            Question {currentIndex + 1} of {questions.length}
          </p>
        </div>
        <select
          value={selectedCategory}
          onChange={(e) => handleCategoryChange(e.target.value)}
          className="input w-64"
          disabled={isLoading}
        >
          <option value="">All Categories</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {loadingState === 'questions' && <Loading text="Loading questions..." />}

      {currentQuestion && loadingState !== 'questions' && (
        <>
          {/* Question Card */}
          <div className="card">
            <div className="flex items-start justify-between gap-4 mb-4">
              <h2 className="text-2xl font-semibold flex-1">{currentQuestion.question}</h2>
              <div className="flex gap-2">
                <span className="badge-primary">{currentQuestion.category}</span>
                <span className="badge-warning">{currentQuestion.difficulty}</span>
              </div>
            </div>

            {currentQuestion.hints && currentQuestion.hints.length > 0 && (
              <div className="mt-4 p-4 bg-[var(--bg-tertiary)] rounded-lg">
                <p className="text-sm font-medium mb-2">Hints:</p>
                <ul className="text-sm text-[var(--text-secondary)] space-y-1">
                  {currentQuestion.hints.map((hint, idx) => (
                    <li key={idx}>• {hint}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Your Answer */}
          <div className="card">
            <label className="block mb-2 font-medium">Your Answer</label>
            <textarea
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="Type your answer here..."
              className="textarea h-48"
              disabled={isLoading}
            />
            <div className="mt-4 flex gap-3">
              <button
                onClick={handleEvaluate}
                disabled={!userAnswer.trim() || isLoading}
                className="btn-primary"
              >
                {loadingState === 'evaluation' ? 'Evaluating...' : 'Evaluate My Answer'}
              </button>
              <button
                onClick={handleGenerateAnswer}
                disabled={isLoading}
                className="btn-secondary"
              >
                {loadingState === 'answer' ? 'Generating...' : 'Show Model Answer'}
              </button>
            </div>
          </div>

          {/* Model Answer */}
          {modelAnswer && (
            <div className="space-y-6 animate-fade-in">
              {/* Summary */}
              <div className="card border-l-4 border-blue-500">
                <h3 className="text-sm font-bold text-blue-400 uppercase tracking-wider mb-2">Summary</h3>
                <p className="text-lg font-medium leading-relaxed">{modelAnswer.summary}</p>
              </div>

              {/* Key Points */}
              <div className="card">
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="text-yellow-400">🔑</span> Key Points
                </h3>
                <ul className="space-y-3">
                  {modelAnswer.key_points.map((point, index) => (
                    <li key={index} className="flex items-start gap-3 text-[var(--text-secondary)]">
                      <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-[var(--text-primary)] shrink-0" />
                      {point}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Detailed Answer */}
              <div className="card">
                <h3 className="text-lg font-bold mb-4">📝 Detailed Answer</h3>
                <div className="prose prose-invert max-w-none text-[var(--text-secondary)] whitespace-pre-wrap leading-relaxed">
                  {modelAnswer.detailed_answer}
                </div>
              </div>

              {/* Examples */}
              {modelAnswer.examples && modelAnswer.examples.length > 0 && (
                <div className="card bg-[var(--bg-secondary)]">
                  <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
                    <span className="text-cyan-400">💡</span> Examples
                  </h3>
                  <ul className="space-y-2">
                    {modelAnswer.examples.map((example, index) => (
                      <li key={index} className="flex items-start gap-2 text-sm font-mono text-[var(--text-secondary)]">
                        <span className="text-cyan-400 mt-1">›</span>
                        {example}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Evaluation */}
          {evaluation && (
            <div className="card">
              <h3 className="text-2xl font-bold mb-6">Evaluation Results</h3>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Score Ring */}
                <div className="flex justify-center">
                  <ScoreRing score={evaluation.scores.overall} size="lg" />
                </div>

                {/* Detailed Scores */}
                <div className="lg:col-span-2 space-y-3">
                  {Object.entries(evaluation.scores)
                    .filter(([key]) => key !== 'overall')
                    .map(([key, value]) => (
                      <div key={key}>
                        <div className="flex justify-between mb-1">
                          <span className="capitalize">{key}</span>
                          <span className="font-semibold">{value.toFixed(1)}/10</span>
                        </div>
                        <div className="h-2 bg-[var(--bg-tertiary)] rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-[var(--accent-primary)] to-[var(--accent-secondary)] transition-all duration-1000"
                            style={{ width: `${(value / 10) * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                </div>
              </div>

              {/* Strengths */}
              {evaluation.strengths.length > 0 && (
                <div className="mt-6">
                  <h4 className="font-semibold text-[var(--success)] mb-3">Strengths</h4>
                  <ul className="space-y-2">
                    {evaluation.strengths.map((strength, idx) => (
                      <li key={idx} className="flex gap-2">
                        <span className="text-[var(--success)]">✓</span>
                        <span className="text-[var(--text-secondary)]">{strength}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Improvements */}
              {evaluation.improvements.length > 0 && (
                <div className="mt-6">
                  <h4 className="font-semibold text-[var(--warning)] mb-3">Areas for Improvement</h4>
                  <ul className="space-y-2">
                    {evaluation.improvements.map((improvement, idx) => (
                      <li key={idx} className="flex gap-2">
                        <span className="text-[var(--warning)]">→</span>
                        <span className="text-[var(--text-secondary)]">{improvement}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Follow-up Questions */}
              {evaluation.follow_up_questions.length > 0 && (
                <div className="mt-6">
                  <h4 className="font-semibold mb-3">Potential Follow-up Questions</h4>
                  <ul className="space-y-2">
                    {evaluation.follow_up_questions.map((question, idx) => (
                      <li key={idx} className="text-[var(--text-secondary)]">
                        {idx + 1}. {question}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Navigation */}
          <div className="flex justify-between">
            <button
              onClick={handlePrevious}
              disabled={currentIndex === 0 || isLoading}
              className="btn-secondary"
            >
              ← Previous Question
            </button>
            <button
              onClick={handleNext}
              disabled={currentIndex >= questions.length - 1 || isLoading}
              className="btn-secondary"
            >
              Next Question →
            </button>
          </div>
        </>
      )}
    </div>
  );
}
