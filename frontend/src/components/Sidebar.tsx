import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  DocumentTextIcon,
  AcademicCapIcon,
  ChartBarIcon,
  LightBulbIcon,
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import { useState } from 'react';

const navigation = [
  { name: 'Home', href: '/', icon: HomeIcon },
  { name: 'Job Analysis', href: '/job-analysis', icon: DocumentTextIcon },
  { name: 'Practice', href: '/practice', icon: AcademicCapIcon },
  { name: 'Progress', href: '/progress', icon: ChartBarIcon },
  { name: 'Term Explainer', href: '/explainer', icon: LightBulbIcon },
];

export default function Sidebar() {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(true);

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-50 lg:hidden btn-secondary"
      >
        {isOpen ? (
          <XMarkIcon className="w-6 h-6" />
        ) : (
          <Bars3Icon className="w-6 h-6" />
        )}
      </button>

      {/* Sidebar */}
      <div
        className={`
          fixed top-0 left-0 h-screen bg-[var(--bg-secondary)] 
          border-r border-[var(--border-color)] 
          transition-transform duration-300 z-40
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 w-64
        `}
      >
        {/* Logo */}
        <div className="h-16 flex items-center px-6 border-b border-[var(--border-color)]">
          <h1 className="text-xl font-bold">
            <span className="text-gradient">AI Interview</span>
            <span className="text-[var(--text-secondary)]"> Assistant</span>
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-6 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={isActive ? 'nav-link-active' : 'nav-link'}
                onClick={() => setIsOpen(false)}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-6 border-t border-[var(--border-color)]">
          <div className="text-xs text-[var(--text-tertiary)]">
            <p>Powered by</p>
            <p className="text-[var(--text-secondary)] font-medium mt-1">
              Groq API (Llama 3.3 70B)
            </p>
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
