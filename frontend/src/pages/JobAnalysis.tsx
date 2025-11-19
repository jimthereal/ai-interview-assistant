import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeJobDescription, analyzeJobDescriptionFile, analyzeJobDescriptionURL } from '../api/client';
import { useAppStore } from '../store';
import Loading from '../components/Loading';
import type { JobDescriptionResponse } from '../types';

type InputMode = 'text' | 'file' | 'url';

export default function JobAnalysis() {
  const [inputMode, setInputMode] = useState<InputMode>('text');
  const [jobDescription, setJobDescription] = useState('');
  const [url, setUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<JobDescriptionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { currentJobAnalysis, setJobAnalysis } = useAppStore();
  const navigate = useNavigate();
  const setCurrentQuestion = useAppStore((state) => state.setCurrentQuestion);
  const resetQuestion = useAppStore((state) => state.resetQuestion);

  // Load persisted analysis on mount
  useEffect(() => {
    if (currentJobAnalysis && !analysis) {
      setAnalysis(currentJobAnalysis);
    }
  }, [currentJobAnalysis, analysis]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const fileType = file.name.toLowerCase();
      if (!fileType.endsWith('.pdf') && !fileType.endsWith('.docx') && !fileType.endsWith('.doc')) {
        setError('Only PDF and DOCX files are supported');
        return;
      }
      setSelectedFile(file);
      setError('');
    }
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError('');

    try {
      let result: JobDescriptionResponse;

      if (inputMode === 'text') {
        if (!jobDescription.trim() || jobDescription.length < 50) {
          setError('Please enter a job description (at least 50 characters)');
          return;
        }
        result = await analyzeJobDescription(jobDescription);
      } else if (inputMode === 'file') {
        if (!selectedFile) {
          setError('Please select a file');
          return;
        }
        result = await analyzeJobDescriptionFile(selectedFile);
      } else {
        // URL mode
        if (!url.trim()) {
          setError('Please enter a URL');
          return;
        }
        // Basic URL validation
        try {
          new URL(url);
        } catch {
          setError('Please enter a valid URL (e.g., https://example.com/job)');
          return;
        }
        result = await analyzeJobDescriptionURL(url);
      }

      setAnalysis(result);
      setJobAnalysis(result);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to analyze job description. Please try again.';
      setError(errorMsg);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const isAnalyzeDisabled = () => {
    if (isLoading) return true;
    if (inputMode === 'text') return jobDescription.length < 50;
    if (inputMode === 'file') return !selectedFile;
    if (inputMode === 'url') return !url.trim();
    return false;
  };

  return (
    <div className="space-y-8 animate-slide-in">
      <div>
        <h1 className="text-4xl font-bold mb-2">Job Description Analysis</h1>
        <p className="text-[var(--text-secondary)]">
          Analyze job descriptions from text, file, or URL to get matched interview questions
        </p>
      </div>

      {/* Input Mode Tabs */}
      <div className="card">
        <div className="flex gap-2 mb-6 border-b border-[var(--border)]">
          <button
            onClick={() => {
              setInputMode('text');
              setError('');
            }}
            className={`px-4 py-2 font-medium transition-colors relative ${
              inputMode === 'text'
                ? 'text-[var(--primary)] after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[var(--primary)]'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            📝 Paste Text
          </button>
          <button
            onClick={() => {
              setInputMode('file');
              setError('');
            }}
            className={`px-4 py-2 font-medium transition-colors relative ${
              inputMode === 'file'
                ? 'text-[var(--primary)] after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[var(--primary)]'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            📄 Upload File
          </button>
          <button
            onClick={() => {
              setInputMode('url');
              setError('');
            }}
            className={`px-4 py-2 font-medium transition-colors relative ${
              inputMode === 'url'
                ? 'text-[var(--primary)] after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-[var(--primary)]'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
            }`}
          >
            🔗 Paste URL
          </button>
        </div>

        {/* Text Input Mode */}
        {inputMode === 'text' && (
          <>
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
            </div>
          </>
        )}

        {/* File Upload Mode */}
        {inputMode === 'file' && (
          <div className="space-y-4">
            <div>
              <label className="block mb-2 font-medium">Upload Document</label>
              <p className="text-sm text-[var(--text-secondary)] mb-4">
                Supported formats: PDF (.pdf), Word (.docx, .doc)
              </p>
            </div>
            <div className="border-2 border-dashed border-[var(--border)] rounded-lg p-8 text-center hover:border-[var(--primary)] transition-colors">
              <input
                type="file"
                id="file-upload"
                accept=".pdf,.docx,.doc"
                onChange={handleFileChange}
                className="hidden"
                disabled={isLoading}
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer flex flex-col items-center"
              >
                <svg
                  className="w-12 h-12 mb-4 text-[var(--text-tertiary)]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                {selectedFile ? (
                  <div className="space-y-1">
                    <p className="font-medium text-[var(--primary)]">
                      {selectedFile.name}
                    </p>
                    <p className="text-sm text-[var(--text-tertiary)]">
                      {(selectedFile.size / 1024).toFixed(2)} KB
                    </p>
                    <p className="text-sm text-[var(--text-secondary)]">
                      Click to change file
                    </p>
                  </div>
                ) : (
                  <div className="space-y-1">
                    <p className="font-medium">Click to upload</p>
                    <p className="text-sm text-[var(--text-tertiary)]">
                      or drag and drop
                    </p>
                  </div>
                )}
              </label>
            </div>
          </div>
        )}

        {/* URL Input Mode */}
        {inputMode === 'url' && (
          <div className="space-y-4">
            <div>
              <label className="block mb-2 font-medium">Job Posting URL</label>
              <p className="text-sm text-[var(--text-secondary)] mb-4">
                Enter a link to a job posting from sites like JobStreet, LinkedIn, Indeed, etc.
              </p>
            </div>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.jobstreet.com.my/job/..."
              className="w-full px-4 py-3 bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/20"
              disabled={isLoading}
            />
          </div>
        )}

        <div className="mt-6 flex items-center justify-end">
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzeDisabled()}
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
                  onClick={() => {
                    resetQuestion();
                    setCurrentQuestion(question);
                    navigate('/practice/question');
                  }}
                  className="p-4 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg hover:border-[var(--accent-primary)] hover:bg-[var(--bg-elevated)] cursor-pointer transition-all duration-200 hover:scale-[1.01]"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <p className="font-medium mb-2 hover:text-[var(--accent-primary)] transition-colors">{question.question}</p>
                      <div className="flex gap-2">
                        <span className="badge-primary text-xs">{question.category}</span>
                        <span className="badge-warning text-xs">{question.difficulty}</span>
                      </div>
                    </div>
                    <div className="flex-shrink-0">
                      <svg
                        className="w-5 h-5 text-[var(--text-tertiary)]"
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
          </div>
        </div>
      )}
    </div>
  );
}
