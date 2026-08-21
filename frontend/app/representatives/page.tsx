'use client';
import { useState, useEffect } from 'react';

export default function RepresentativesPage() {
  const [reps, setReps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReps();
  }, []);

  const fetchReps = async () => {
    try {
      const res = await fetch('/api/v1/representatives/');
      if (!res.ok) throw new Error('Failed to load representatives');
      const data = await res.json();
      setReps(data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-8 w-full max-w-7xl mx-auto py-8">
      <div className="flex justify-between items-end">
        <div className="space-y-4">
          <h1 className="text-4xl font-extrabold text-gray-900">Representatives</h1>
          <p className="text-lg text-gray-500">
            Directory of Members of Parliament and Legislative Assemblies.
          </p>
        </div>
        <div className="flex space-x-4">
          <select className="border border-gray-300 rounded-md py-2 px-4 text-sm text-gray-700 outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">All States</option>
          </select>
          <select className="border border-gray-300 rounded-md py-2 px-4 text-sm text-gray-700 outline-none focus:ring-2 focus:ring-blue-500">
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
          <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200">
            <p className="font-medium">Failed to load data</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {!loading && !error && reps.length === 0 && (
          <div className="flex flex-col items-center justify-center space-y-4 text-gray-400 py-24 border border-dashed border-gray-300 rounded-xl bg-gray-50">
            <svg className="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            <p className="text-lg font-medium text-gray-500">DATA_NOT_AVAILABLE</p>
            <p className="text-sm">No representative profiles found in the database.</p>
          </div>
        )}

        {!loading && !error && reps.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">House</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Constituency</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">State</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Party</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {reps.map((rep, idx) => (
                  <tr key={idx} className="hover:bg-gray-50 cursor-pointer">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">{rep.full_name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rep.house}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rep.constituency}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rep.state}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rep.party}</td>
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
