interface ErrorStateProps {
  message: string;
  requestId?: string;
  onRetry?: () => void;
}

export function ErrorState({ message, requestId, onRetry }: ErrorStateProps) {
  return (
    <div className="bg-red-50 text-red-800 p-6 rounded-xl border border-red-200 max-w-2xl mx-auto my-6 space-y-4">
      <div className="flex items-start space-x-3">
        <svg className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div className="space-y-1">
          <h3 className="font-bold text-lg">An API Error Occurred</h3>
          <p className="text-sm text-red-700">{message}</p>
        </div>
      </div>
      
      {requestId && (
        <div className="bg-red-100/50 rounded-lg p-3 text-xs font-mono flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <span>TraceNest Debug ID: <span className="font-bold select-all">{requestId}</span></span>
          <span className="text-[10px] text-red-500 uppercase tracking-wider font-semibold">Report to Admin</span>
        </div>
      )}

      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-semibold transition-colors"
        >
          Retry Request
        </button>
      )}
    </div>
  );
}
