import { useExplainerStore } from '../store/explainerStore';
import { explainTerm } from '../api/client';
import Loading from '../components/Loading';

export default function Explainer() {
  const {
    term,
    result,
    isLoading,
    error,
    setTerm,
    setResult,
    setIsLoading,
    setError
  } = useExplainerStore();

  const handleExplain = async () => {
    if (!term.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const data = await explainTerm(term);
      setResult(data);
    } catch (err) {
      console.error('Failed to explain term:', err);
      setError('Failed to get explanation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8 animate-slide-in max-w-4xl mx-auto">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Technical Term Explainer
        </h1>
        <p className="text-[var(--text-secondary)] text-lg">
          Master complex concepts with simple, structured explanations
        </p>
      </div>

      <div className="card p-6 shadow-lg border border-[var(--border-color)]">
        <div className="flex gap-4">
          <input
            type="text"
            value={term}
            onChange={(e) => setTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleExplain()}
            placeholder="Enter a technical term (e.g., Kubernetes, OAuth, Big O)..."
            className="input flex-1 text-lg py-3"
            disabled={isLoading}
          />
          <button
            onClick={handleExplain}
            disabled={!term.trim() || isLoading}
            className="btn-primary px-8 text-lg font-semibold"
          >
            {isLoading ? 'Analyzing...' : 'Explain'}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-center">
          {error}
        </div>
      )}

      {isLoading && <Loading text="Generating structured explanation..." />}

      {result && !isLoading && (
        <div className="space-y-6 animate-fade-in">
          {/* Definition Section */}
          <div className="card border-l-4 border-blue-500">
            <h3 className="text-sm font-bold text-blue-400 uppercase tracking-wider mb-2">Definition</h3>
            <p className="text-xl font-medium leading-relaxed">{result.definition}</p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Analogy Section */}
            <div className="card border-l-4 border-purple-500">
              <h3 className="text-sm font-bold text-purple-400 uppercase tracking-wider mb-2">
                💡 Real-World Analogy
              </h3>
              <p className="text-[var(--text-secondary)] italic">"{result.analogy}"</p>
            </div>

            {/* Why It Matters Section */}
            <div className="card border-l-4 border-green-500">
              <h3 className="text-sm font-bold text-green-400 uppercase tracking-wider mb-2">
                🚀 Why It Matters
              </h3>
              <p className="text-[var(--text-secondary)]">{result.why_it_matters}</p>
            </div>
          </div>

          {/* Key Points Section */}
          <div className="card">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <span className="text-yellow-400">🔑</span> Key Concepts
            </h3>
            <ul className="space-y-3">
              {result.key_points.map((point, index) => (
                <li key={index} className="flex items-start gap-3 text-[var(--text-secondary)]">
                  <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-[var(--text-primary)] shrink-0" />
                  {point}
                </li>
              ))}
            </ul>
          </div>

          {/* Example Section */}
          <div className="card bg-[var(--bg-secondary)]">
            <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
              <span className="text-cyan-400">💻</span> Technical Example
            </h3>
            <div className="bg-[var(--bg-primary)] p-4 rounded-lg font-mono text-sm border border-[var(--border-color)]">
              {result.example}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
