import { useState, useEffect } from 'react';
import { useAppStore } from '../store';
import Loading from '../components/Loading';
import ScoreRing from '../components/ScoreRing';

export default function Progress() {
  const [isLoading, setIsLoading] = useState(true);
  const practiceHistory = useAppStore((state) => state.practiceHistory);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setIsLoading(false), 500);
  }, []);

  if (isLoading) {
    return <Loading text="Loading progress..." />;
  }

  if (practiceHistory.length === 0) {
    return (
      <div className="text-center py-12 animate-slide-in">
        <h1 className="text-4xl font-bold mb-4">Progress Dashboard</h1>
        <p className="text-[var(--text-secondary)] mb-8">
          Start practicing to see your progress here
        </p>
        <a href="/practice" className="btn-primary inline-block">
          Start Practicing
        </a>
      </div>
    );
  }

  // Calculate statistics from practice history
  const totalQuestions = practiceHistory.length;
  const scores = practiceHistory
    .filter((p) => p.evaluation?.scores.overall)
    .map((p) => p.evaluation!.scores.overall);
  const averageScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;

  // Category breakdown
  const categoryStats: Record<string, { count: number; totalScore: number; scores: number[] }> = {};
  practiceHistory.forEach((practice) => {
    const category = practice.question.category;
    if (!categoryStats[category]) {
      categoryStats[category] = { count: 0, totalScore: 0, scores: [] };
    }
    categoryStats[category].count++;
    if (practice.evaluation?.scores.overall) {
      categoryStats[category].totalScore += practice.evaluation.scores.overall;
      categoryStats[category].scores.push(practice.evaluation.scores.overall);
    }
  });

  // Calculate trend
  let trend = 'Stable →';
  if (scores.length >= 4) {
    const firstHalf = scores.slice(0, Math.floor(scores.length / 2));
    const secondHalf = scores.slice(Math.floor(scores.length / 2));
    const firstAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;

    if (secondAvg > firstAvg + 0.5) {
      trend = 'Improving ↗';
    } else if (secondAvg < firstAvg - 0.5) {
      trend = 'Declining ↘';
    }
  }

  return (
    <div className="space-y-8 animate-slide-in">
      <h1 className="text-4xl font-bold">Progress Dashboard</h1>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-4xl font-bold text-gradient">
            {totalQuestions}
          </div>
          <div className="text-[var(--text-secondary)] mt-2">Questions Practiced</div>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-2">
            <ScoreRing score={averageScore} size="md" showLabel={true} />
          </div>
          <div className="text-[var(--text-secondary)]">Average Score</div>
        </div>

        <div className="card text-center">
          <div className="text-4xl font-bold text-gradient">
            {Object.keys(categoryStats).length}
          </div>
          <div className="text-[var(--text-secondary)] mt-2">Categories Practiced</div>
          <div className="text-sm text-[var(--accent-primary)] mt-1">{trend}</div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">Performance by Category</h2>
        <div className="space-y-4">
          {Object.entries(categoryStats).map(([category, stats]) => {
            const avgScore = stats.totalScore / stats.count;
            return (
              <div key={category}>
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">{category}</span>
                  <span className="text-sm text-[var(--text-secondary)]">
                    {stats.count} questions • Avg: {avgScore.toFixed(1)}/10
                  </span>
                </div>
                <div className="h-2 bg-[var(--bg-tertiary)] rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-[var(--accent-primary)] to-[var(--accent-secondary)] transition-all duration-500"
                    style={{ width: `${(avgScore / 10) * 100}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Practice History */}
      {practiceHistory.length > 0 && (
        <div className="card">
          <h2 className="text-2xl font-bold mb-6">Recent Practice</h2>
          <div className="space-y-4">
            {practiceHistory.slice(-10).reverse().map((practice, idx) => (
              <div
                key={idx}
                className="p-4 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="badge-primary text-xs">{practice.question.category}</span>
                      <span className="text-xs text-[var(--text-tertiary)]">
                        {new Date(practice.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="font-medium mb-2">{practice.question.question}</p>
                  </div>
                  {practice.evaluation && (
                    <div className="flex-shrink-0">
                      <ScoreRing score={practice.evaluation.scores.overall} size="sm" />
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Improvement Suggestions */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">💡 Suggestions</h2>
        <ul className="space-y-3">
          {averageScore < 7 && (
            <li className="flex items-start gap-2">
              <span className="text-yellow-400 mt-1">•</span>
              <span className="text-[var(--text-secondary)]">
                Focus on providing more detailed and structured answers
              </span>
            </li>
          )}
          {Object.entries(categoryStats).filter(([, stats]) => (stats.totalScore / stats.count) < 6).map(([category]) => (
            <li key={category} className="flex items-start gap-2">
              <span className="text-yellow-400 mt-1">•</span>
              <span className="text-[var(--text-secondary)]">
                Practice more {category} questions to improve in this area
              </span>
            </li>
          ))}
          {averageScore >= 8 && (
            <li className="flex items-start gap-2">
              <span className="text-green-400 mt-1">•</span>
              <span className="text-[var(--text-secondary)]">
                Great job! Try tackling harder questions or new categories
              </span>
            </li>
          )}
          {totalQuestions < 5 && (
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span className="text-[var(--text-secondary)]">
                Consistency is key! Try to practice regularly for best results
              </span>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}
