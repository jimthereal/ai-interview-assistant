interface ScoreRingProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

export default function ScoreRing({ score, size = 'md', showLabel = true }: ScoreRingProps) {
  const sizes = {
    sm: { width: 60, stroke: 4, text: 'text-lg' },
    md: { width: 80, stroke: 5, text: 'text-2xl' },
    lg: { width: 120, stroke: 6, text: 'text-4xl' },
  };

  const { width, stroke, text } = sizes[size];
  const radius = (width - stroke) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (score / 10) * circumference;

  // Color based on score
  const getColor = (score: number) => {
    if (score >= 8) return 'var(--success)';
    if (score >= 6) return 'var(--warning)';
    return 'var(--error)';
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={width} height={width} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={width / 2}
          cy={width / 2}
          r={radius}
          fill="none"
          stroke="var(--border-color)"
          strokeWidth={stroke}
        />
        {/* Progress circle */}
        <circle
          cx={width / 2}
          cy={width / 2}
          r={radius}
          fill="none"
          stroke={getColor(score)}
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
        {/* Score text */}
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dy=".3em"
          className={`${text} font-bold fill-[var(--text-primary)] transform rotate-90`}
          style={{ transformOrigin: 'center' }}
        >
          {score.toFixed(1)}
        </text>
      </svg>
      {showLabel && (
        <span className="text-xs text-[var(--text-secondary)] font-medium">
          Overall Score
        </span>
      )}
    </div>
  );
}
