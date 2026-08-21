'use client';
import { useState, useEffect } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

type ConflictRecord = {
  entity_id: string;
  field: string;
  status: string;
  observations: { source_id: string; value: unknown }[];
  requires_review: boolean;
};

export default function DataQualityPage() {
  const [conflicts, setConflicts] = useState<ConflictRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  useEffect(() => {
    fetchConflicts();
  }, []);

  const fetchConflicts = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchApi('/data-quality/conflicts');
      setConflicts(data.data || []);
    } catch (err: any) {
      setError({
        message: err.message || 'Failed to load data quality records.',
        requestId: err.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Data Quality Index</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Monitor data conflicts, reconciliation logs, and overall database health.
        </p>
      </div>

      {/* Health cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        {[
          { label: 'Total Conflicts', value: conflicts.length, color: 'red' },
          { label: 'Requiring Review', value: conflicts.filter((c) => c.requires_review).length, color: 'amber' },
          { label: 'Data Sources', value: 'INSUFFICIENT_DATA', color: 'gray' },
        ].map((stat) => (
          <div key={stat.label} className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5 shadow-sm">
            <p className={`text-2xl font-extrabold ${stat.color === 'red' ? 'text-red-600 dark:text-red-400' : stat.color === 'amber' ? 'text-amber-600 dark:text-amber-400' : 'text-gray-400 dark:text-gray-600'}`}>
              {stat.value}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Conflicts table */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Data Conflicts</h2>
        {loading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        )}

        {error && (
          <ErrorState
            message={error.message}
            requestId={error.requestId}
            onRetry={fetchConflicts}
          />
        )}

        {!loading && !error && conflicts.length === 0 && (
          <div className="empty-state py-16 dark:bg-slate-900/30 animate-fadeIn">
            <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-lg font-medium text-gray-500 dark:text-gray-400">No conflicts detected</p>
            <p className="text-sm text-gray-400 dark:text-gray-500">DATABASE_EMPTY — no records to reconcile</p>
          </div>
        )}

        {!loading && !error && conflicts.length > 0 && (
          <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm animate-fadeIn">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-slate-800">
              <thead className="bg-gray-50 dark:bg-slate-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Entity ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Field</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Review</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-slate-900 divide-y divide-gray-200 dark:divide-slate-800">
                {conflicts.map((c, i) => (
                  <tr key={i}>
                    <td className="px-6 py-4 text-sm font-mono text-gray-700 dark:text-gray-300">{c.entity_id}</td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{c.field}</td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-400">
                        {c.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {c.requires_review ? (
                        <span className="text-amber-600 dark:text-amber-400 font-medium">Required</span>
                      ) : (
                        'No'
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
