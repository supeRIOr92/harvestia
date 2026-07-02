import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { PrivyClientProvider } from '@/lib/privy'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
title: 'Harvestia',
description: 'Farm, explore, trade.',
}

export default function RootLayout({
children,
}: {
children: React.ReactNode
}) {
return (
<html lang="en">
<body className={inter.className}>
<PrivyClientProvider>
{children}
</PrivyClientProvider>
</body>
</html>
)
}
