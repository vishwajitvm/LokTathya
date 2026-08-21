'use client';
import { useState } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

type CompareResult = {
  rep_a?: string;
  rep_b?: string;
  [key: string]: unknown;
};

export default function ComparePage() {
  const [repA, setRepA] = useState('');
  const [repB, setRepB] = useState('');
  const [result, setResult] = useState<CompareResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  const handleCompare = async () => {
    if (!repA.trim() || !repB.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await fetchApi(
        `/intelligence/compare/representatives?rep_a=${encodeURIComponent(repA)}&rep_b=${encodeURIComponent(repB)}`
      );
      setResult(data);
    } catch (e: any) {
      setError({
        message: e.message || 'Comparison failed.',
        requestId: e.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-5xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Comparison Tool</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Compare representatives, constituencies, and historical elections side-by-side.
        </p>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-2xl shadow-sm p-6 space-y-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">Compare Representatives</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Representative A (ID or name)
            </label>
            <input
              type="text"
              value={repA}
              onChange={(e) => setRepA(e.target.value)}
              placeholder="e.g. uuid-1234"
              className="w-full border border-gray-300 dark:border-slate-800 bg-white dark:bg-slate-850 text-gray-900 dark:text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Representative B (ID or name)
            </label>
            <input
              type="text"
              value={repB}
              onChange={(e) => setRepB(e.target.value)}
              placeholder="e.g. uuid-5678"
              className="w-full border border-gray-300 dark:border-slate-800 bg-white dark:bg-slate-850 text-gray-900 dark:text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <button
          onClick={handleCompare}
          disabled={!repA.trim() || !repB.trim() || loading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Comparing…' : 'Compare'}
        </button>

        {error && (
          <ErrorState
            message={error.message}
            requestId={error.requestId}
            onRetry={handleCompare}
          />
        )}

        {result && (
          <div className="bg-gray-50 dark:bg-slate-950/40 rounded-xl p-4 border border-gray-200 dark:border-slate-800 animate-fadeIn">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Comparison Result</h3>
            <pre className="text-xs text-gray-700 dark:text-gray-300 overflow-auto whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}

        {!result && !loading && !error && (
          <div className="empty-state py-12 dark:bg-slate-900/30">
            <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p className="text-sm text-gray-500 dark:text-gray-400">Enter two representative IDs above to compare.</p>
          </div>
        )}
      </div>
    </div>
  );
}
