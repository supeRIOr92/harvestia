'use client'

import { usePrivy } from '@privy-io/react-auth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Home() {
const { ready, authenticated, login } = usePrivy()
const router = useRouter()

useEffect(() => {
if (ready && authenticated) {
router.push('/onboarding')
}
}, [ready, authenticated, router])

return (
<main className="min-h-screen bg-green-950 flex flex-col items-center justify-center">
<div className="text-center space-y-6">
<h1 className="text-6xl font-bold text-green-300 tracking-tight">
Harvestia
</h1>
<p className="text-green-400 text-xl">
Farm, explore, trade.
</p>
<button
onClick={login}
disabled={!ready}
className="mt-8 px-8 py-4 bg-green-500 hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl text-lg transition-colors"
>
{ready ? 'Connect Wallet' : 'Loading...'}
</button>
</div>
</main>
)
}
