import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'ClauseWise AI — Contract Intelligence', description: 'Evidence-first insurance contract analysis' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="fr"><body>{children}</body></html>; }
