'use client'

import { PrivyProvider } from '@privy-io/react-auth'

export function PrivyClientProvider({ children }: { children: React.ReactNode }) {
return (
<PrivyProvider
appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID!}
config={{
appearance: {
theme: 'dark',
accentColor: '#4ade80',
},
}}
>
{children}
</PrivyProvider>
)
}
