import { useState } from 'react';
import { explainTerm } from '../api/client';
import Loading from '../components/Loading';
import { marked } from 'marked';

export default function Explainer() {
  const [term, setTerm] = useState('');
  const [submittedTerm, setSubmittedTerm] = useState(''); // Track submitted term
  const [explanation, setExplanation] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleExplain = async () => {
    if (!term.trim()) return;

    setIsLoading(true);
    setSubmittedTerm(term); // Save the term that was submitted
    try {
      const result = await explainTerm(term);
      setExplanation(result.explanation);
    } catch (error) {
      console.error('Failed to explain term:', error);
      setExplanation('Failed to get explanation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Convert markdown to HTML
  const renderMarkdown = (text: string) => {
    return { __html: marked(text) };
  };

  return (
    <div className="space-y-8 animate-slide-in">
      <div>
        <h1 className="text-4xl font-bold mb-2">Technical Term Explainer</h1>
        <p className="text-[var(--text-secondary)]">
          Enter any technical term to get a clear, beginner-friendly explanation
        </p>
      </div>

      <div className="card">
        <label className="block mb-2 font-medium">Term to Explain</label>
        <div className="flex gap-3">
          <input
            type="text"
            value={term}
            onChange={(e) => setTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleExplain()}
            placeholder="e.g., REST API, Docker, Microservices..."
            className="input flex-1"
            disabled={isLoading}
          />
          <button
            onClick={handleExplain}
            disabled={!term.trim() || isLoading}
            className="btn-primary"
          >
            Explain
          </button>
        </div>
      </div>

      {isLoading && <Loading text="Generating explanation..." />}

      {explanation && !isLoading && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-4">{submittedTerm}</h2>
          <div 
            className="prose prose-invert max-w-none text-[var(--text-secondary)] leading-relaxed"
            dangerouslySetInnerHTML={renderMarkdown(explanation)}
          />
        </div>
      )}
    </div>
  );
}
