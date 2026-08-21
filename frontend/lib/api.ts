export const fetchApi = async (endpoint: string, options?: RequestInit) => {
  const response = await fetch(`/api/v1${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  const requestId = response.headers.get('X-Request-ID');

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message = errorData.detail || errorData.message || 'An API error occurred';
    const error = new Error(message) as Error & { requestId?: string; status?: number };
    error.requestId = requestId || errorData.request_id || 'UNKNOWN';
    error.status = response.status;
    throw error;
  }

  return response.json();
};
