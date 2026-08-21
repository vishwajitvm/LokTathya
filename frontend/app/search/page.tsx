'use client';
import { useState, useEffect } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (query.trim()) {
        fetchResults(query);
      } else {
        setResults([]);
      }
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  const fetchResults = async (searchQuery: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchApi(`/search/?query=${encodeURIComponent(searchQuery)}`);
      setResults(data.data || []);
    } catch (err: any) {
      setError({
        message: err.message || 'Failed to fetch search results.',
        requestId: err.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-4xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-4">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Search LokTathya</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Search for representatives, constituencies, elections, and civic data.
        </p>
      </div>

      <div className="w-full">
        <div className="relative flex items-center w-full h-14 rounded-lg focus-within:shadow-lg bg-white dark:bg-slate-900 overflow-hidden border border-gray-300 dark:border-slate-800">
          <div className="grid place-items-center h-full w-12 text-gray-300 dark:text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            className="peer h-full w-full outline-none text-sm text-gray-700 dark:text-gray-200 pr-2 bg-transparent"
            type="text"
            id="search"
            placeholder="Search by name, state, district..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="w-full pt-8">
        {!query && (
          <div className="flex flex-col items-center justify-center space-y-4 text-gray-400 dark:text-gray-500 py-16 border-2 border-dashed border-gray-200 dark:border-slate-800 rounded-xl">
            <svg className="w-16 h-16 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <p className="text-lg font-medium text-gray-500 dark:text-gray-400">Type a query to begin searching.</p>
            <p className="text-sm text-gray-400 dark:text-gray-500">Search works across representatives, elections, and geographies.</p>
          </div>
        )}

        {loading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        )}

        {error && (
          <ErrorState
            message={error.message}
            requestId={error.requestId}
            onRetry={() => fetchResults(query)}
          />
        )}

        {!loading && !error && query && results.length === 0 && (
          <div className="flex flex-col items-center justify-center space-y-4 text-gray-400 dark:text-gray-500 py-16 border border-gray-200 dark:border-slate-800 rounded-xl bg-gray-50 dark:bg-slate-900/30">
            <p className="text-lg font-medium text-gray-600 dark:text-gray-300 font-semibold">No results found for "{query}"</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Try adjusting your search terms.</p>
          </div>
        )}

        {!loading && !error && results.length > 0 && (
          <ul className="space-y-4">
            {results.map((item, idx) => (
              <li key={idx} className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-4 rounded-xl shadow-sm">
                <p className="text-gray-900 dark:text-gray-200">{item.text || JSON.stringify(item)}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
