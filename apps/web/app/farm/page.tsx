'use client'

import { usePrivy } from '@privy-io/react-auth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function FarmPage() {
const { ready, authenticated } = usePrivy()
const router = useRouter()

useEffect(() => {
if (ready && !authenticated) {
router.push('/')
}
}, [ready, authenticated, router])

if (!ready) return null

return (
<main className="min-h-screen bg-green-950 flex flex-col items-center justify-center">
<div className="text-center space-y-4">
<h1 className="text-4xl font-bold text-green-300">Your Farm</h1>
<p className="text-green-500">Sprint 2 — coming soon</p>
</div>
</main>
)
}
