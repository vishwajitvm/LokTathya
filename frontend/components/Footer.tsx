export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="bg-white dark:bg-slate-900 border-t border-gray-200 dark:border-slate-800 mt-auto transition-colors duration-200">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
              <span className="text-white font-black text-xs">L</span>
            </div>
            <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">LokTathya</span>
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
            &copy; {year} LokTathya Civic Data Platform &mdash; Open Source, Neutral, Verified
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500">
            Data from official government sources only
          </p>
        </div>
      </div>
    </footer>
  );
}
