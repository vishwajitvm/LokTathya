'use client';
import { useState } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

const REPORT_TYPES = [
  { value: 'election_summary', label: 'Election Summary' },
  { value: 'representative_profile', label: 'Representative Profile' },
  { value: 'constituency_overview', label: 'Constituency Overview' },
];

const SCOPES = [
  { value: 'national', label: 'National' },
  { value: 'state', label: 'State' },
  { value: 'constituency', label: 'Constituency' },
];

type ReportResult = { [key: string]: unknown };

export default function ReportsPage() {
  const [reportType, setReportType] = useState('election_summary');
  const [scope, setScope] = useState('national');
  const [result, setResult] = useState<ReportResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await fetchApi(
        `/intelligence/reports?report_type=${reportType}&scope=${scope}`,
        { method: 'POST' }
      );
      setResult(data);
    } catch (e: any) {
      setError({
        message: e.message || 'Report generation failed.',
        requestId: e.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-5xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Civic Reports</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Generate comprehensive civic data reports based on verified database records.
        </p>
      </div>

      <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-2xl shadow-sm p-6 space-y-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">Generate Report</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Report Type</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full border border-gray-300 dark:border-slate-800 bg-white dark:bg-slate-850 text-gray-900 dark:text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {REPORT_TYPES.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Scope</label>
            <select
              value={scope}
              onChange={(e) => setScope(e.target.value)}
              className="w-full border border-gray-300 dark:border-slate-800 bg-white dark:bg-slate-850 text-gray-900 dark:text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {SCOPES.map((s) => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Generating…' : 'Generate Report'}
        </button>

        {error && (
          <ErrorState
            message={error.message}
            requestId={error.requestId}
            onRetry={handleGenerate}
          />
        )}

        {result && (
          <div className="bg-gray-50 dark:bg-slate-950/40 rounded-xl p-4 border border-gray-200 dark:border-slate-800 animate-fadeIn">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-gray-900 dark:text-white">Report Output</h3>
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {REPORT_TYPES.find((t) => t.value === reportType)?.label} — {SCOPES.find((s) => s.value === scope)?.label}
              </span>
            </div>
            <pre className="text-xs text-gray-700 dark:text-gray-300 overflow-auto whitespace-pre-wrap max-h-96">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}

        {!result && !loading && !error && (
          <div className="empty-state py-12 dark:bg-slate-900/30">
            <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-sm text-gray-500 dark:text-gray-400">Select a report type and scope, then click Generate.</p>
          </div>
        )}
      </div>
    </div>
  );
}
