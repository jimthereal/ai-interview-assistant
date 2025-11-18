import { useState, useEffect } from 'react';
import { getProgress } from '../api/client';
import Loading from '../components/Loading';
import ScoreRing from '../components/ScoreRing';
import type { ProgressResponse } from '../types';

export default function Progress() {
  const [data, setData] = useState<ProgressResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const result = await getProgress();
      setData(result);
    } catch (error) {
      console.error('Failed to load progress:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loading text="Loading progress..." />;
  }

  if (!data || data.stats.total_questions_practiced === 0) {
    return (
      <div className="text-center py-12 animate-slide-in">
        <h1 className="text-4xl font-bold mb-4">Progress Dashboard</h1>
        <p className="text-[var(--text-secondary)] mb-8">
          Start practicing to see your progress here
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-slide-in">
      <h1 className="text-4xl font-bold">Progress Dashboard</h1>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-4xl font-bold text-gradient">
            {data.stats.total_questions_practiced}
          </div>
          <div className="text-[var(--text-secondary)] mt-2">Questions Practiced</div>
        </div>
        
        <div className="card flex justify-center items-center">
          <ScoreRing score={data.stats.average_score} size="md" showLabel={true} />
        </div>

        <div className="card text-center">
          <div className="text-4xl font-bold text-gradient">
            {Object.keys(data.stats.category_breakdown).length}
          </div>
          <div className="text-[var(--text-secondary)] mt-2">Categories Covered</div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">Performance by Category</h2>
        <div className="space-y-4">
          {Object.entries(data.stats.category_breakdown).map(([category, stats]) => (
            <div key={category}>
              <div className="flex justify-between mb-2">
                <span className="font-medium">{category}</span>
                <span className="text-[var(--text-secondary)]">
                  {stats.count} questions • Avg: {stats.average_score.toFixed(1)}/10
                </span>
              </div>
              <div className="h-3 bg-[var(--bg-tertiary)] rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-[var(--accent-primary)] to-[var(--accent-secondary)]"
                  style={{ width: `${(stats.average_score / 10) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Practices */}
      {data.stats.recent_practices.length > 0 && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-6">Recent Practice Sessions</h2>
          <div className="space-y-3">
            {data.stats.recent_practices.map((practice, idx) => (
              <div
                key={idx}
                className="p-4 bg-[var(--bg-tertiary)] rounded-lg flex items-center justify-between"
              >
                <div className="flex-1">
                  <p className="font-medium mb-1">{practice.question}</p>
                  <span className="badge-primary text-xs">{practice.category}</span>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-gradient">
                    {practice.score.toFixed(1)}
                  </div>
                  <div className="text-xs text-[var(--text-tertiary)]">
                    {new Date(practice.timestamp).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Suggestions */}
      {data.improvement_suggestions.length > 0 && (
        <div className="card bg-[var(--bg-elevated)]">
          <h2 className="text-2xl font-bold mb-4">Improvement Suggestions</h2>
          <ul className="space-y-2">
            {data.improvement_suggestions.map((suggestion, idx) => (
              <li key={idx} className="flex gap-2 text-[var(--text-secondary)]">
                <span className="text-[var(--accent-primary)]">→</span>
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
