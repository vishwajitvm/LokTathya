import './globals.css';

export const metadata = {
  title: 'LokTathya',
  description: 'LokTathya Civic Data Platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
