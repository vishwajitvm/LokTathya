'use client';
import { useState, useEffect } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

export default function RepresentativesPage() {
  const [reps, setReps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  useEffect(() => {
    fetchReps();
  }, []);

  const fetchReps = async () => {
    try {
      const data = await fetchApi('/representatives/');
      setReps(data || []);
    } catch (err: any) {
      setError({
        message: err.message || 'Failed to load representatives.',
        requestId: err.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8 transition-colors duration-200">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div className="space-y-4">
          <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Representatives</h1>
          <p className="text-lg text-gray-500 dark:text-gray-400">
            Directory of Members of Parliament and Legislative Assemblies.
          </p>
        </div>
        <div className="flex space-x-4 w-full sm:w-auto">
          <select className="border border-gray-300 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-md py-2 px-4 text-sm text-gray-700 dark:text-gray-300 outline-none focus:ring-2 focus:ring-blue-500 w-1/2 sm:w-auto">
            <option value="">All States</option>
          </select>
          <select className="border border-gray-300 dark:border-slate-800 bg-white dark:bg-slate-900 rounded-md py-2 px-4 text-sm text-gray-700 dark:text-gray-300 outline-none focus:ring-2 focus:ring-blue-500 w-1/2 sm:w-auto">
            <option value="">Lok Sabha</option>
            <option value="">Rajya Sabha</option>
            <option value="">Vidhan Sabha</option>
          </select>
        </div>
      </div>

      <div className="w-full">
        {loading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        )}

        {error && (
          <ErrorState
            message={error.message}
            requestId={error.requestId}
            onRetry={fetchReps}
          />
        )}

        {!loading && !error && reps.length === 0 && (
          <div className="flex flex-col items-center justify-center space-y-4 text-gray-400 dark:text-gray-500 py-24 border border-dashed border-gray-300 dark:border-slate-800 rounded-xl bg-gray-50 dark:bg-slate-900/30 animate-fadeIn">
            <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            <p className="text-lg font-medium text-gray-500 dark:text-gray-400">DATA_NOT_AVAILABLE</p>
            <p className="text-sm">No representative profiles found in the database.</p>
          </div>
        )}

        {!loading && !error && reps.length > 0 && (
          <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-slate-800">
              <thead className="bg-gray-50 dark:bg-slate-800">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Name</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">House</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Constituency</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">State</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Party</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-slate-900 divide-y divide-gray-200 dark:divide-slate-800">
                {reps.map((rep, idx) => (
                  <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-slate-800/40 cursor-pointer">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600 dark:text-blue-400">{rep.full_name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{rep.house}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{rep.constituency}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{rep.state}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{rep.party}</td>
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
