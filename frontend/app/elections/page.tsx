'use client';
import { useState, useEffect } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

export default function ElectionsPage() {
  const [elections, setElections] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  useEffect(() => {
    fetchElections();
  }, []);

  const fetchElections = async () => {
    try {
      const data = await fetchApi('/elections/');
      setElections(data.data || []);
    } catch (err: any) {
      setError({
        message: err.message || 'Failed to load elections.',
        requestId: err.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-4">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Historical Elections</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Analyze historical election results, candidate data, and voting trends.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-8">
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-8 shadow-sm">
          <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg flex items-center justify-center mb-6">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Lok Sabha</h2>
          <p className="text-gray-500 dark:text-gray-400 mb-6">General elections to the lower house of India's Parliament.</p>
          <button className="px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-700 text-gray-700 dark:text-gray-300 rounded-md text-sm font-medium hover:bg-gray-50 dark:hover:bg-slate-700">
            View Lok Sabha Elections
          </button>
        </div>

        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-8 shadow-sm">
          <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 rounded-lg flex items-center justify-center mb-6">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"></path></svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Vidhan Sabha</h2>
          <p className="text-gray-500 dark:text-gray-400 mb-6">State legislative assembly elections across India.</p>
          <button className="px-4 py-2 bg-white dark:bg-slate-800 border border-gray-300 dark:border-slate-700 text-gray-700 dark:text-gray-300 rounded-md text-sm font-medium hover:bg-gray-50 dark:hover:bg-slate-700">
            View Assembly Elections
          </button>
        </div>
      </div>

      <div className="w-full pt-8 mt-8 border-t border-gray-200 dark:border-slate-800">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">Recent Elections Datasets</h3>
        
        {loading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        )}

        {error && (
          <ErrorState
            message={error.message}
            requestId={error.requestId}
            onRetry={fetchElections}
          />
        )}

        {!loading && !error && elections.length === 0 && (
          <div className="flex flex-col items-center justify-center space-y-4 text-gray-400 dark:text-gray-500 py-16 border border-dashed border-gray-300 dark:border-slate-800 rounded-xl bg-gray-50 dark:bg-slate-900/30">
            <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            <p className="text-lg font-medium text-gray-500 dark:text-gray-400">DATA_NOT_AVAILABLE</p>
            <p className="text-sm">No historical election datasets found in the database.</p>
          </div>
        )}
      </div>
    </div>
  );
}
