import Link from 'next/link';

const features = [
  {
    href: '/geography',
    title: 'Geography',
    desc: 'Explore states, districts, and historical constituency boundary changes.',
    color: 'blue',
    icon: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  },
  {
    href: '/representatives',
    title: 'Representatives',
    desc: 'Search profiles of MPs and MLAs with cross-referenced election records.',
    color: 'indigo',
    icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
  },
  {
    href: '/elections',
    title: 'Elections',
    desc: 'Analyse historical election results, candidates, and voting trends.',
    color: 'emerald',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
  },
  {
    href: '/projects',
    title: 'Projects',
    desc: 'Track infrastructure and developmental projects funded through public budgets.',
    color: 'amber',
    icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
  },
  {
    href: '/finance',
    title: 'Finance',
    desc: 'Analyse budgets, expenditure, and financial disclosures of civic entities.',
    color: 'teal',
    icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  },
  {
    href: '/civic-ai',
    title: 'Civic AI',
    desc: 'Ask natural-language questions about India\'s civic data with citations.',
    color: 'purple',
    icon: 'M13 10V3L4 14h7v7l9-11h-7z',
  },
];

const colorMap: Record<string, string> = {
  blue:   'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 group-hover:bg-blue-600 group-hover:text-white',
  indigo: 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 group-hover:bg-indigo-600 group-hover:text-white',
  emerald:'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 group-hover:bg-emerald-600 group-hover:text-white',
  amber:  'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 group-hover:bg-amber-600 group-hover:text-white',
  teal:   'bg-teal-100 dark:bg-teal-900/30 text-teal-600 dark:text-teal-400 group-hover:bg-teal-600 group-hover:text-white',
  purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 group-hover:bg-purple-600 group-hover:text-white',
};

export default function HomePage() {
  return (
    <div className="flex flex-col space-y-12 py-8 transition-colors duration-200">
      {/* Hero */}
      <div className="text-center space-y-6 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 bg-blue-50 dark:bg-blue-950/20 text-blue-700 dark:text-blue-300 text-xs font-semibold px-3 py-1 rounded-full border border-blue-200 dark:border-blue-900/30">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
          Open Civic Data Platform
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white tracking-tight leading-tight">
          Civic Truth,{' '}
          <span className="text-blue-600 dark:text-blue-500">Verified.</span>
        </h1>
        <p className="text-lg sm:text-xl text-gray-500 dark:text-gray-400 leading-relaxed">
          LokTathya provides a transparent, auditable platform for India&apos;s historical
          election data, civic geography, and representative records — all sourced
          from official government databases.
        </p>

        {/* Search bar (navigates to /search) */}
        <div className="w-full max-w-2xl mx-auto pt-4">
          <Link
            href="/search"
            className="relative flex items-center w-full h-14 rounded-xl bg-white dark:bg-slate-900 overflow-hidden border border-gray-300 dark:border-slate-800 hover:border-blue-400 dark:hover:border-blue-500 hover:shadow-md transition-all group"
          >
            <div className="grid place-items-center h-full w-12 text-gray-400 dark:text-gray-500 group-hover:text-blue-500">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <span className="text-sm text-gray-400 dark:text-gray-500 group-hover:text-gray-600 dark:group-hover:text-gray-300">
              Search for a representative, constituency, or election…
            </span>
          </Link>
        </div>
      </div>

      {/* Stats bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Lok Sabha Seats', value: '543' },
          { label: 'States & UTs', value: '36' },
          { label: 'Data Source', value: 'ECI' },
          { label: 'Data Type', value: 'Verified' },
        ].map((stat) => (
          <div key={stat.label} className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-4 text-center shadow-sm">
            <p className="text-2xl font-extrabold text-blue-600 dark:text-blue-500">{stat.value}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Feature cards */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Explore Civic Data</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feat) => (
            <Link
              key={feat.href}
              href={feat.href}
              className="group block bg-white dark:bg-slate-900 rounded-xl border border-gray-200 dark:border-slate-800 shadow-sm hover:shadow-md hover:border-blue-300 dark:hover:border-blue-500 transition-all p-6"
            >
              <div className="flex items-center space-x-4 mb-4">
                <div className={`p-3 rounded-lg transition-colors ${colorMap[feat.color]}`}>
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={feat.icon} />
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">{feat.title}</h3>
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{feat.desc}</p>
              <div className="mt-4 flex items-center text-sm text-blue-600 dark:text-blue-500 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                Explore →
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/30 rounded-xl p-4">
        <p className="text-sm text-amber-800 dark:text-amber-300">
          <strong>Data Integrity Notice:</strong> All civic data on LokTathya is sourced exclusively from official government
          databases (ECI, Ministry of Finance, etc.). Where data conflicts exist, they are flagged as{' '}
          <code className="bg-amber-100 dark:bg-amber-900/40 px-1 rounded">DATA_DISCREPANCY</code> and not silently resolved.
          We never fabricate civic statistics.
        </p>
      </div>
    </div>
  );
}
