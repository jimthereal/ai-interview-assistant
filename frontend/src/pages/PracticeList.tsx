import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getQuestions, getCategories } from '../api/client';
import { useAppStore } from '../store';
import Loading from '../components/Loading';
import type { Question } from '../types';

export default function PracticeList() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [displayCount, setDisplayCount] = useState(20); // Lazy loading - show 20 initially
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const setCurrentQuestion = useAppStore((state) => state.setCurrentQuestion);
  const resetQuestion = useAppStore((state) => state.resetQuestion);

  useEffect(() => {
    loadCategories();
    loadQuestions();
  }, []);

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      console.log('Loaded categories:', data.categories);
      setCategories(data.categories);
    } catch (error) {
      console.error('Failed to load categories:', error);
      setError('Failed to load categories');
    }
  };

  const loadQuestions = async (category?: string) => {
    setIsLoading(true);
    setError('');
    try {
      const data = await getQuestions({
        category: category || undefined,
        limit: 150,
      });
      console.log('Loaded questions:', data.questions.length, data.questions[0]);
      setQuestions(data.questions);
      if (data.questions.length === 0) {
        setError('No questions loaded from API');
      }
    } catch (error) {
      console.error('Failed to load questions:', error);
      setError('Failed to load questions. Please check if backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    setDisplayCount(20); // Reset to first page
    loadQuestions(category || undefined);
  };

  const handleQuestionClick = (question: Question) => {
    resetQuestion();
    setCurrentQuestion(question);
    navigate('/practice/question');
  };

  const filteredQuestions = questions.filter((q) =>
    q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
    q.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const displayedQuestions = filteredQuestions.slice(0, displayCount);
  const hasMore = displayedQuestions.length < filteredQuestions.length;

  const loadMore = () => {
    setDisplayCount((prev) => prev + 20);
  };

  if (isLoading) {
    return <Loading text="Loading questions..." />;
  }

  if (error) {
    return (
      <div className="text-center py-12 animate-slide-in">
        <h1 className="text-4xl font-bold mb-4">Practice Interview Questions</h1>
        <div className="card max-w-2xl mx-auto bg-[var(--error)]/10 border border-[var(--error)]/20">
          <p className="text-[var(--error)] mb-4">{error}</p>
          <button onClick={() => loadQuestions()} className="btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  const difficultyColors = {
    Easy: 'text-green-400',
    Medium: 'text-yellow-400',
    Hard: 'text-red-400',
  };

  return (
    <div className="space-y-8 animate-slide-in">
      <div>
        <h1 className="text-4xl font-bold mb-2">Practice Interview Questions</h1>
        <p className="text-[var(--text-secondary)]">
          Choose a question to practice. Get AI-generated answers and detailed feedback.
        </p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Category Filter */}
          <div>
            <label className="block mb-2 text-sm font-medium">Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => handleCategoryChange(e.target.value)}
              className="input"
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {/* Search */}
          <div>
            <label className="block mb-2 text-sm font-medium">Search</label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search questions..."
              className="input"
            />
          </div>
        </div>

        <div className="mt-4 text-sm text-[var(--text-tertiary)]">
          Showing {displayedQuestions.length} of {filteredQuestions.length} questions
          {filteredQuestions.length !== questions.length && ` (filtered from ${questions.length} total)`}
        </div>
      </div>

      {/* Questions List */}
      <div className="space-y-4">
        {displayedQuestions.map((question, index) => (
          <div
            key={question.id || index}
            onClick={() => handleQuestionClick(question)}
            className="card hover:bg-[var(--bg-elevated)] cursor-pointer transition-all duration-200 hover:scale-[1.01] hover:shadow-lg"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="badge badge-primary">{question.category}</span>
                  <span className={`text-sm font-medium ${difficultyColors[question.difficulty as keyof typeof difficultyColors]}`}>
                    {question.difficulty}
                  </span>
                </div>
                <h3 className="text-lg font-medium mb-2 hover:text-[var(--accent-primary)] transition-colors">
                  {question.question}
                </h3>
                {question.hints && question.hints.length > 0 && (
                  <p className="text-sm text-[var(--text-tertiary)] line-clamp-2">
                    💡 {question.hints[0]}
                  </p>
                )}
              </div>
              <div className="flex-shrink-0">
                <svg
                  className="w-6 h-6 text-[var(--text-tertiary)]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Load More Button */}
      {hasMore && (
        <div className="text-center">
          <button onClick={loadMore} className="btn-secondary">
            Load More Questions ({filteredQuestions.length - displayedQuestions.length} remaining)
          </button>
        </div>
      )}

      {filteredQuestions.length === 0 && (
        <div className="text-center py-12">
          <p className="text-[var(--text-secondary)]">
            No questions found matching your criteria
          </p>
        </div>
      )}
    </div>
  );
}
