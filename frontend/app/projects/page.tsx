'use client';
import { useState, useEffect } from 'react';

const FILTERS = ['All', 'Ongoing', 'Completed', 'Stalled'];

export default function ProjectsPage() {
  const [activeFilter, setActiveFilter] = useState('All');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 600);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Civic Projects</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Track infrastructure and developmental projects funded through public budgets.
        </p>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2">
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setActiveFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors border ${
              activeFilter === f
                ? 'bg-blue-600 text-white border-blue-600'
                : 'bg-white dark:bg-slate-900 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-slate-800 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        </div>
      ) : (
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden animate-fadeIn">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-slate-800 flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white">Projects — {activeFilter}</h2>
            <span className="text-xs text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-slate-800 px-2 py-1 rounded">Official records only</span>
          </div>
          <div className="empty-state py-16 dark:bg-slate-900/30">
            <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            <p className="text-lg font-medium text-gray-500 dark:text-gray-400">DATA_NOT_AVAILABLE</p>
            <p className="text-sm text-gray-400 dark:text-gray-500">No project records found in the database.</p>
          </div>
        </div>
      )}
    </div>
  );
}
