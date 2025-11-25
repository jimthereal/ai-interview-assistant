import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateAnswer, evaluateAnswer } from '../api/client';
import { useAppStore } from '../store';
import Loading from '../components/Loading';
import ScoreRing from '../components/ScoreRing';

export default function PracticeQuestion() {
  const navigate = useNavigate();

  const {
    currentQuestion,
    currentAnswer,
    setCurrentAnswer,
    modelAnswer,
    setModelAnswer,
    evaluation,
    setEvaluation,
    isLoading,
    setIsLoading,
    addPracticeEntry,
  } = useAppStore();

  useEffect(() => {
    if (!currentQuestion) {
      navigate('/practice');
    }
  }, [currentQuestion, navigate]);

  if (!currentQuestion) {
    return <Loading text="Loading question..." />;
  }

  const handleGenerateAnswer = async () => {
    setIsLoading(true);
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
    }
  };

  const handleEvaluate = async () => {
    if (!currentAnswer.trim()) return;

    setIsLoading(true);
    try {
      const result = await evaluateAnswer({
        question: currentQuestion.question,
        user_answer: currentAnswer,
        category: currentQuestion.category,
        difficulty: currentQuestion.difficulty,
        model_answer: modelAnswer?.detailed_answer || undefined,
      });
      setEvaluation(result);

      // Add to practice history
      addPracticeEntry({
        question: currentQuestion,
        userAnswer: currentAnswer,
        modelAnswer: modelAnswer,
        evaluation: result,
        timestamp: new Date(),
      });
    } catch (error) {
      console.error('Failed to evaluate answer:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/practice');
  };

  return (
    <div className="space-y-8 animate-slide-in">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button onClick={handleBack} className="btn-ghost">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Questions
        </button>
      </div>

      {/* Question Card */}
      <div className="card-elevated">
        <div className="flex items-center gap-3 mb-4">
          <span className="badge badge-primary">{currentQuestion.category}</span>
          <span className="text-sm font-medium text-[var(--accent-secondary)]">
            {currentQuestion.difficulty}
          </span>
        </div>
        <h1 className="text-3xl font-bold mb-4">{currentQuestion.question}</h1>
        {currentQuestion.hints && currentQuestion.hints.length > 0 && (
          <div className="bg-[var(--bg-tertiary)] border-l-4 border-[var(--accent-primary)] p-4 rounded">
            <p className="text-sm text-[var(--text-secondary)]">
              💡 <strong>Hint:</strong> {currentQuestion.hints[0]}
            </p>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="flex gap-2 mb-6 border-b border-[var(--border-color)]">
          <button className="px-4 py-2 border-b-2 border-[var(--accent-primary)] text-[var(--accent-primary)] font-medium">
            Your Answer
          </button>
        </div>

        {/* Your Answer Section */}
        <div className="space-y-4">
          <textarea
            value={currentAnswer}
            onChange={(e) => setCurrentAnswer(e.target.value)}
            placeholder="Write your answer here...&#10;&#10;Think about:&#10;• Key concepts and definitions&#10;• Real-world examples&#10;• Trade-offs and considerations"
            className="textarea h-64"
            disabled={isLoading}
          />

          <div className="flex gap-3">
            <button
              onClick={handleEvaluate}
              disabled={!currentAnswer.trim() || isLoading}
              className="btn-primary"
            >
              {isLoading ? 'Evaluating...' : 'Evaluate My Answer'}
            </button>
            <button
              onClick={handleGenerateAnswer}
              disabled={isLoading}
              className="btn-secondary"
            >
              {isLoading ? 'Generating...' : 'Show Model Answer'}
            </button>
          </div>
        </div>
      </div>

      {/* Model Answer */}
      {modelAnswer && !isLoading && (
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

      {/* Evaluation Results */}
      {evaluation && !isLoading && (
        <div className="space-y-6">
          <div className="card">
            <h2 className="text-2xl font-bold mb-6">📊 Evaluation Results</h2>

            {/* Score Overview */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
              <div className="text-center">
                <ScoreRing score={evaluation.scores.overall} size="lg" />
                <p className="text-sm text-[var(--text-secondary)] mt-2">Overall</p>
              </div>
              <div className="text-center">
                <ScoreRing score={evaluation.scores.clarity} size="md" />
                <p className="text-sm text-[var(--text-secondary)] mt-2">Clarity</p>
              </div>
              <div className="text-center">
                <ScoreRing score={evaluation.scores.completeness} size="md" />
                <p className="text-sm text-[var(--text-secondary)] mt-2">Complete</p>
              </div>
              <div className="text-center">
                <ScoreRing score={evaluation.scores.accuracy} size="md" />
                <p className="text-sm text-[var(--text-secondary)] mt-2">Accuracy</p>
              </div>
              <div className="text-center">
                <ScoreRing score={evaluation.scores.professionalism} size="md" />
                <p className="text-sm text-[var(--text-secondary)] mt-2">Professional</p>
              </div>
            </div>

            {/* Feedback */}
            {evaluation.feedback && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-3">Overall Feedback</h3>
                <p className="text-[var(--text-secondary)]">{evaluation.feedback}</p>
              </div>
            )}

            {/* Strengths */}
            {evaluation.strengths && evaluation.strengths.length > 0 && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-3 text-green-400">✅ Strengths</h3>
                <ul className="space-y-2">
                  {evaluation.strengths.map((strength, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-green-400 mt-1">•</span>
                      <span className="text-[var(--text-secondary)]">{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Improvements */}
            {evaluation.improvements && evaluation.improvements.length > 0 && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-3 text-yellow-400">💡 Areas for Improvement</h3>
                <ul className="space-y-2">
                  {evaluation.improvements.map((improvement, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-yellow-400 mt-1">•</span>
                      <span className="text-[var(--text-secondary)]">{improvement}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Follow-up Questions */}
            {evaluation.follow_up_questions && evaluation.follow_up_questions.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3">🤔 Potential Follow-up Questions</h3>
                <ul className="space-y-2">
                  {evaluation.follow_up_questions.map((question, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-[var(--accent-primary)] mt-1">•</span>
                      <span className="text-[var(--text-secondary)]">{question}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button onClick={handleBack} className="btn-primary">
              Practice Another Question
            </button>
          </div>
        </div>
      )}

      {isLoading && <Loading text="Processing..." />}
    </div>
  );
}
