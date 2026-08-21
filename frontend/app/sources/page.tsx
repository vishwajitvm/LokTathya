'use client';
import { useState, useEffect } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

type Source = {
  id: string;
  name: string;
  official_url?: string;
  category?: string;
  last_fetched?: string;
};

export default function SourcesPage() {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  useEffect(() => {
    fetchSources();
  }, []);

  const fetchSources = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchApi('/sources/');
      setSources(Array.isArray(data) ? data : []);
    } catch (err: any) {
      setError({
        message: err.message || 'Failed to load sources.',
        requestId: err.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Data Sources &amp; Provenance</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          View the official origins and provenance of all civic data ingested into LokTathya.
        </p>
      </div>

      <div className="bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/30 rounded-xl p-4">
        <p className="text-sm text-blue-800 dark:text-blue-300">
          <strong>Provenance guarantee:</strong> Every data record in LokTathya is linked to its source
          document. No data is published without a verifiable official citation.
        </p>
      </div>

      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {error && (
        <ErrorState
          message={error.message}
          requestId={error.requestId}
          onRetry={fetchSources}
        />
      )}

      {!loading && !error && sources.length === 0 && (
        <div className="empty-state py-16 dark:bg-slate-900/30">
          <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <p className="text-lg font-medium text-gray-500 dark:text-gray-400">DATA_NOT_AVAILABLE</p>
          <p className="text-sm text-gray-400 dark:text-gray-500">No sources have been registered in the database yet.</p>
        </div>
      )}

      {!loading && !error && sources.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 animate-fadeIn">
          {sources.map((src) => (
            <div key={src.id} className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5 space-y-3 shadow-sm">
              <div className="flex items-start justify-between">
                <h3 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">{src.name}</h3>
                {src.category && (
                  <span className="text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 px-2 py-0.5 rounded-full">
                    {src.category}
                  </span>
                )}
              </div>
              {src.official_url && (
                <a
                  href={src.official_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-600 dark:text-blue-400 hover:underline truncate block"
                >
                  {src.official_url}
                </a>
              )}
              {src.last_fetched && (
                <p className="text-xs text-gray-400 dark:text-gray-500">
                  Last fetched: {new Date(src.last_fetched).toLocaleDateString('en-IN')}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
