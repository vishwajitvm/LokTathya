'use client';
import { useState, useEffect } from 'react';
import { fetchApi } from '../../lib/api';
import { ErrorState } from '../../components/ErrorState';

export default function GeographyPage() {
  const [selectedState, setSelectedState] = useState('');
  const [geographies, setGeographies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; requestId?: string } | null>(null);

  useEffect(() => {
    fetchGeographies();
  }, []);

  const fetchGeographies = async () => {
    try {
      const data = await fetchApi('/geographies/');
      setGeographies(data.data || []);
    } catch (err: any) {
      setError({
        message: err.message || 'Failed to load geographies.',
        requestId: err.requestId,
      });
    } finally {
      setLoading(false);
    }
  };

  const states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"];

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8 transition-colors duration-200">
      <div className="space-y-4">
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white">Civic Geography</h1>
        <p className="text-lg text-gray-500 dark:text-gray-400">
          Explore India's states, districts, and parliamentary constituencies.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="md:col-span-1 border-r border-gray-200 dark:border-slate-800 pr-4 h-[calc(100vh-200px)] overflow-y-auto">
          <h3 className="text-sm font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-4">States & UTs</h3>
          <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
            {states.map(state => (
              <li key={state}>
                <button 
                  onClick={() => setSelectedState(state)}
                  className={`w-full text-left px-3 py-2 rounded-md transition-colors ${selectedState === state ? 'bg-blue-50 dark:bg-slate-800 text-blue-700 dark:text-blue-400 font-medium' : 'hover:bg-gray-100 dark:hover:bg-slate-800'}`}
                >
                  {state}
                </button>
              </li>
            ))}
          </ul>
        </div>
        
        <div className="md:col-span-3">
          {error && (
            <ErrorState
              message={error.message}
              requestId={error.requestId}
              onRetry={fetchGeographies}
            />
          )}

          {!error && selectedState ? (
            <div className="space-y-6 animate-fadeIn">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">{selectedState}</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
                  <h4 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Districts</h4>
                  <p className="text-3xl font-bold mt-2 text-gray-400 dark:text-gray-600">DATA_NOT_AVAILABLE</p>
                </div>
                <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
                  <h4 className="text-gray-500 dark:text-gray-400 text-sm font-medium">Constituencies</h4>
                  <p className="text-3xl font-bold mt-2 text-gray-400 dark:text-gray-600">DATA_NOT_AVAILABLE</p>
                </div>
              </div>
              <div className="w-full h-96 bg-gray-100 dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl flex items-center justify-center text-gray-400 dark:text-gray-600">
                <p>Map rendering unavailable (INSUFFICIENT_DATA)</p>
              </div>
            </div>
          ) : !error && (
            <div className="w-full h-full flex flex-col items-center justify-center space-y-4 text-gray-400 dark:text-gray-500 py-32 border-2 border-dashed border-gray-200 dark:border-slate-800 rounded-xl">
              <svg className="w-16 h-16 text-gray-300 dark:text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p className="text-lg font-medium text-gray-500 dark:text-gray-400">Select a state to explore.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
