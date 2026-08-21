import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center space-y-12 py-16">
      <div className="text-center space-y-6 max-w-3xl">
        <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight">
          Civic Truth, <span className="text-blue-600">Verified.</span>
        </h1>
        <p className="text-xl text-gray-500">
          LokTathya provides a transparent, auditable platform for India's historical election data, civic geography, and representative records.
        </p>
        
        <div className="w-full max-w-2xl mx-auto pt-6">
          <div className="relative flex items-center w-full h-14 rounded-lg focus-within:shadow-lg bg-white overflow-hidden border border-gray-300">
            <div className="grid place-items-center h-full w-12 text-gray-300">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              className="peer h-full w-full outline-none text-sm text-gray-700 pr-2 bg-transparent"
              type="text"
              id="search"
              placeholder="Search for a representative, constituency, or election..."
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full pt-12">
        
        <Link href="/geography" className="group block bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-blue-300 transition-all p-6">
          <div className="flex items-center space-x-4 mb-4">
            <div className="bg-blue-100 p-3 rounded-lg text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <h3 className="text-lg font-bold text-gray-900">Geography</h3>
          </div>
          <p className="text-sm text-gray-500">Explore states, districts, and historical constituency boundary changes.</p>
        </Link>

        <Link href="/representatives" className="group block bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-blue-300 transition-all p-6">
          <div className="flex items-center space-x-4 mb-4">
            <div className="bg-indigo-100 p-3 rounded-lg text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </div>
            <h3 className="text-lg font-bold text-gray-900">Representatives</h3>
          </div>
          <p className="text-sm text-gray-500">Search profiles of MPs and MLAs with cross-referenced election data.</p>
        </Link>

        <Link href="/elections" className="group block bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-blue-300 transition-all p-6">
          <div className="flex items-center space-x-4 mb-4">
            <div className="bg-emerald-100 p-3 rounded-lg text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
            <h3 className="text-lg font-bold text-gray-900">Elections</h3>
          </div>
          <p className="text-sm text-gray-500">Analyze historical election results, candidate data, and voting trends.</p>
        </Link>
        
      </div>
    </div>
  );
}
