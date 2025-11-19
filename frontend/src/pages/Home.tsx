import { Link } from 'react-router-dom';
import {
  DocumentTextIcon,
  AcademicCapIcon,
  ChartBarIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';

const features = [
  {
    name: 'Job Description Analysis',
    description: 'Paste any job description and get AI-powered analysis of required skills and tailored interview questions.',
    icon: DocumentTextIcon,
    href: '/job-analysis',
    color: 'from-orange-500 to-red-500',
  },
  {
    name: 'Practice Interview Questions',
    description: 'Access 150+ curated questions across technical and behavioral topics with AI-generated model answers.',
    icon: AcademicCapIcon,
    href: '/practice',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    name: 'Track Your Progress',
    description: 'Monitor your practice sessions, scores, and improvement trends across different question categories.',
    icon: ChartBarIcon,
    href: '/progress',
    color: 'from-purple-500 to-pink-500',
  },
  {
    name: 'Learn Technical Terms',
    description: 'Get clear, beginner-friendly explanations of any technical concept with real-world examples.',
    icon: SparklesIcon,
    href: '/explainer',
    color: 'from-green-500 to-emerald-500',
  },
];

export default function Home() {
  return (
    <div className="space-y-12 animate-slide-in">
      {/* Hero Section */}
      <div className="text-center space-y-6 py-12">
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight">
          <span className="text-gradient">AI-Powered</span>
          <br />
          <span className="text-[var(--text-primary)]">Interview Assistant</span>
        </h1>
        <p className="text-xl text-[var(--text-secondary)] max-w-3xl mx-auto">
          Master technical interviews with personalized practice questions, AI-generated answers, 
          and detailed feedback tailored to your target job.
        </p>
        <div className="flex gap-4 justify-center">
          <Link to="/job-analysis" className="btn-primary text-lg px-8 py-3">
            Get Started
          </Link>
          <Link to="/practice" className="btn-secondary text-lg px-8 py-3">
            Browse Questions
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-4xl font-bold text-gradient">150+</div>
          <div className="text-[var(--text-secondary)] mt-2">Interview Questions</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-gradient">100%</div>
          <div className="text-[var(--text-secondary)] mt-2">Free - No Costs</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-gradient">AI</div>
          <div className="text-[var(--text-secondary)] mt-2">Powered by Llama 3.3</div>
        </div>
      </div>

      {/* Features */}
      <div>
        <h2 className="text-3xl font-bold mb-8">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature) => (
            <Link
              key={feature.name}
              to={feature.href}
              className="card-elevated group hover:scale-105 transition-transform duration-300"
            >
              <div className="flex items-start gap-4">
                <div className={`p-3 rounded-lg bg-gradient-to-br ${feature.color}`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold group-hover:text-gradient transition-colors">
                    {feature.name}
                  </h3>
                  <p className="text-[var(--text-secondary)] mt-2">
                    {feature.description}
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* How It Works */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">How It Works</h2>
        <div className="space-y-6">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[var(--accent-primary)] flex items-center justify-center text-sm font-bold">
              1
            </div>
            <div>
              <h3 className="font-semibold mb-1">Analyze Job Description</h3>
              <p className="text-[var(--text-secondary)]">
                Paste any job posting to extract required skills and get matched interview questions
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[var(--accent-primary)] flex items-center justify-center text-sm font-bold">
              2
            </div>
            <div>
              <h3 className="font-semibold mb-1">Practice with AI Assistance</h3>
              <p className="text-[var(--text-secondary)]">
                Answer questions and generate AI model answers for reference
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[var(--accent-primary)] flex items-center justify-center text-sm font-bold">
              3
            </div>
            <div>
              <h3 className="font-semibold mb-1">Get Detailed Feedback</h3>
              <p className="text-[var(--text-secondary)]">
                Receive comprehensive evaluation with specific improvement suggestions
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[var(--accent-primary)] flex items-center justify-center text-sm font-bold">
              4
            </div>
            <div>
              <h3 className="font-semibold mb-1">Track Your Progress</h3>
              <p className="text-[var(--text-secondary)]">
                Monitor improvement over time and identify areas for focused practice
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="card bg-[var(--bg-elevated)]">
        <h2 className="text-2xl font-bold mb-4">Built With Modern Tech</h2>
        <div className="flex flex-wrap gap-3">
          <span className="badge-primary">FastAPI</span>
          <span className="badge-primary">React</span>
          <span className="badge-primary">TypeScript</span>
          <span className="badge-primary">Groq API</span>
          <span className="badge-primary">ChromaDB</span>
          <span className="badge-primary">Tailwind CSS</span>
        </div>
      </div>
    </div>
  );
}
