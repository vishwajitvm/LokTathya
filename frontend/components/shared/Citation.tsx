import React from 'react';

export interface CitationProps {
  sourceName: string;
  authority: string;
  officialUrl: string;
  documentTitle?: string;
  page?: number;
  retrievedAt: string;
}

export const Citation: React.FC<CitationProps> = ({ sourceName, authority, officialUrl, documentTitle, page, retrievedAt }) => {
  return (
    <div className="border border-gray-200 rounded p-4 text-sm bg-gray-50">
      <h4 className="font-semibold text-gray-800">Source: {sourceName}</h4>
      <p className="text-gray-600">Authority: {authority}</p>
      {documentTitle && <p className="text-gray-600">Document: {documentTitle} {page && `(Page ${page})`}</p>}
      <p className="text-xs text-gray-400 mt-2">Retrieved: {new Date(retrievedAt).toLocaleDateString()}</p>
      <a href={officialUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline mt-1 block">
        View Official Source
      </a>
    </div>
  );
};
