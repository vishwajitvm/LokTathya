'use client';
import { useState, useEffect } from 'react';

export default function GeographyPage() {
  const [selectedState, setSelectedState] = useState('');
  const [geographies, setGeographies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGeographies();
  }, []);

  const fetchGeographies = async () => {
    try {
      const res = await fetch('/api/v1/geographies/');
      if (!res.ok) throw new Error('Failed to load geographies');
      const data = await res.json();
      setGeographies(data.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"];

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8">
      <div className="space-y-4">
        <h1 className="text-4xl font-extrabold text-gray-900">Civic Geography</h1>
        <p className="text-lg text-gray-500">
          Explore India's states, districts, and parliamentary constituencies.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="md:col-span-1 border-r border-gray-200 pr-4 h-[calc(100vh-200px)] overflow-y-auto">
          <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">States & UTs</h3>
          <ul className="space-y-2 text-sm text-gray-700">
            {states.map(state => (
              <li key={state}>
                <button 
                  onClick={() => setSelectedState(state)}
                  className={`w-full text-left px-3 py-2 rounded-md transition-colors ${selectedState === state ? 'bg-blue-50 text-blue-700 font-medium' : 'hover:bg-gray-100'}`}
                >
                  {state}
                </button>
              </li>
            ))}
          </ul>
        </div>
        
        <div className="md:col-span-3">
          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200 mb-6">
              <p className="font-medium">Error loading data</p>
              <p className="text-sm">{error}</p>
            </div>
          )}

          {selectedState ? (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-900">{selectedState}</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                  <h4 className="text-gray-500 text-sm font-medium">Districts</h4>
                  <p className="text-3xl font-bold mt-2 text-gray-400">DATA_NOT_AVAILABLE</p>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                  <h4 className="text-gray-500 text-sm font-medium">Constituencies</h4>
                  <p className="text-3xl font-bold mt-2 text-gray-400">DATA_NOT_AVAILABLE</p>
                </div>
              </div>
              <div className="w-full h-96 bg-gray-100 border border-gray-200 rounded-xl flex items-center justify-center text-gray-400">
                <p>Map rendering unavailable (INSUFFICIENT_DATA)</p>
              </div>
            </div>
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center space-y-4 text-gray-400 py-32 border-2 border-dashed border-gray-200 rounded-xl">
              <svg className="w-16 h-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p className="text-lg font-medium text-gray-500">Select a state to explore.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
