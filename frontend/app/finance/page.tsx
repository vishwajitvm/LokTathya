'use client';
import { useState, useEffect } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

export default function FinancePage() {
  const [loading, setLoading] = useState(true);
  const [utilization, setUtilization] = useState<{ utilization_rate?: number; status?: string } | null>(null);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  useEffect(() => {
    fetchUtilization();
  }, []);

  const fetchUtilization = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchApi('/analytics/financial/utilization?allocated=0&expenditure=0');
      setUtilization(data);
    } catch (err: any) {
      setError({
        message: err.message || 'Failed to load financial utilization analytics.',
        requestId: err.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Financial Disclosures</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Analyse budgets, expenditure, and financial disclosures of civic entities.
        </p>
      </div>

      {/* Overview cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Utilization Rate</p>
          {loading ? (
            <div className="h-8 bg-gray-200 dark:bg-slate-800 animate-pulse rounded w-24" />
          ) : error ? (
            <p className="text-red-500 text-sm">Error</p>
          ) : (
            <p className="text-2xl font-extrabold text-teal-600 dark:text-teal-400">
              {utilization?.utilization_rate !== undefined
                ? `${(utilization.utilization_rate * 100).toFixed(1)}%`
                : 'N/A'}
            </p>
          )}
        </div>
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Total Projects</p>
          <p className="text-2xl font-extrabold text-gray-400 dark:text-gray-600">DATA_NOT_AVAILABLE</p>
        </div>
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Fiscal Year</p>
          <p className="text-2xl font-extrabold text-gray-400 dark:text-gray-600">INSUFFICIENT_DATA</p>
        </div>
      </div>

      {error && (
        <ErrorState
          message={error.message}
          requestId={error.requestId}
          onRetry={fetchUtilization}
        />
      )}

      {/* Table placeholder */}
      <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden animate-fadeIn">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-slate-800 flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Financial Records</h2>
          <span className="text-xs text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-slate-800 px-2 py-1 rounded">Verified sources only</span>
        </div>
        <div className="empty-state py-16 dark:bg-slate-900/30">
          <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-lg font-medium text-gray-500 dark:text-gray-400">DATA_NOT_AVAILABLE</p>
          <p className="text-sm text-gray-400 dark:text-gray-500">No financial records found. Ingest government budget data to populate this view.</p>
        </div>
      </div>
    </div>
  );
}
