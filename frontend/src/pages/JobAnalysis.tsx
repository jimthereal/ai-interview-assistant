import { useState, useEffect } from 'react';
import { analyzeJobDescription } from '../api/client';
import { useAppStore } from '../store';
import Loading from '../components/Loading';
import type { JobDescriptionResponse } from '../types';

export default function JobAnalysis() {
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState<JobDescriptionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { currentJobAnalysis, setJobAnalysis } = useAppStore();

  // Load persisted analysis on mount
  useEffect(() => {
    if (currentJobAnalysis && !analysis) {
      setAnalysis(currentJobAnalysis);
    }
  }, [currentJobAnalysis, analysis]);

  const handleAnalyze = async () => {
    if (!jobDescription.trim() || jobDescription.length < 50) {
      setError('Please enter a job description (at least 50 characters)');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const result = await analyzeJobDescription(jobDescription);
      setAnalysis(result);
      setJobAnalysis(result);
    } catch (err) {
      setError('Failed to analyze job description. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8 animate-slide-in">
      <div>
        <h1 className="text-4xl font-bold mb-2">Job Description Analysis</h1>
        <p className="text-[var(--text-secondary)]">
          Paste a job description to extract key requirements and get matched interview questions
        </p>
      </div>

      {/* Input Section */}
      <div className="card">
        <label className="block mb-2 font-medium">Job Description</label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here...&#10;&#10;Example:&#10;We are looking for a Senior Python Developer with 5+ years of experience...&#10;Required skills: Python, FastAPI, React, PostgreSQL, AWS, Docker..."
          className="textarea h-64"
          disabled={isLoading}
        />
        <div className="mt-4 flex items-center justify-between">
          <span className="text-sm text-[var(--text-tertiary)]">
            {jobDescription.length} characters
          </span>
          <button
            onClick={handleAnalyze}
            disabled={isLoading || jobDescription.length < 50}
            className="btn-primary"
          >
            {isLoading ? 'Analyzing...' : 'Analyze Job Description'}
          </button>
        </div>
        {error && (
          <div className="mt-4 p-4 bg-[var(--error)]/10 border border-[var(--error)]/20 rounded-lg text-[var(--error)]">
            {error}
          </div>
        )}
      </div>

      {/* Loading State */}
      {isLoading && <Loading text="Analyzing job description..." />}

      {/* Results */}
      {analysis && !isLoading && (
        <div className="space-y-6">
          {/* Summary */}
          <div className="card">
            <h2 className="text-2xl font-bold mb-4">Analysis Summary</h2>
            <p className="text-[var(--text-secondary)]">{analysis.summary}</p>
          </div>

          {/* Key Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Required Skills */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Required Skills</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.analysis.required_skills.map((skill, idx) => (
                  <span key={idx} className="badge-primary">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Preferred Skills */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Preferred Skills</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.analysis.preferred_skills.length > 0 ? (
                  analysis.analysis.preferred_skills.map((skill, idx) => (
                    <span key={idx} className="badge-success">
                      {skill}
                    </span>
                  ))
                ) : (
                  <span className="text-[var(--text-tertiary)]">None specified</span>
                )}
              </div>
            </div>

            {/* Job Role */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-2">Job Role</h3>
              <p className="text-[var(--text-secondary)]">{analysis.analysis.job_role}</p>
            </div>

            {/* Experience Level */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-2">Experience Level</h3>
              <p className="text-[var(--text-secondary)]">{analysis.analysis.experience_level}</p>
            </div>
          </div>

          {/* Matched Questions */}
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold">Matched Interview Questions</h2>
                <p className="text-[var(--text-secondary)] mt-1">
                  {analysis.matched_questions.length} questions relevant to this role
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {analysis.matched_questions.map((question, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg hover:border-[var(--border-hover)] transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <p className="font-medium mb-2">{question.question}</p>
                      <div className="flex gap-2">
                        <span className="badge-primary text-xs">{question.category}</span>
                        <span className="badge-warning text-xs">{question.difficulty}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
