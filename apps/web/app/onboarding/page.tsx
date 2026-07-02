'use client'

import { useState, useEffect } from 'react'
import { usePrivy } from '@privy-io/react-auth'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'

export default function OnboardingPage() {
const { ready, authenticated, user } = usePrivy()
const router = useRouter()
const [gender, setGender] = useState<'male' | 'female' | null>(null)
const [username, setUsername] = useState('')
const [loading, setLoading] = useState(false)
const [error, setError] = useState('')

useEffect(() => {
if (ready && !authenticated) {
router.push('/')
}
}, [ready, authenticated, router])

useEffect(() => {
if (!ready || !authenticated || !user) return
const checkUser = async () => {
const wallet = user.wallet?.address
if (!wallet) return
const { data } = await supabase
.from('users')
.select('id')
.eq('wallet_address', wallet)
.single()
if (data) {
router.push('/farm')
}
}
checkUser()
}, [ready, authenticated, user, router])

const handleSubmit = async () => {
if (!gender) return setError('Choose your gender first')
if (!username.trim()) return setError('Farmer name cannot be empty')
if (username.trim().length < 3) return setError('Name must be at least 3 characters')
if (username.trim().length > 20) return setError('Name must be 20 characters or less')

const wallet = user?.wallet?.address
if (!wallet) return setError('Wallet not found')

setLoading(true)
setError('')

const { data: newUser, error: insertError } = await supabase
.from('users')
.insert({ wallet_address: wallet, username: username.trim(), gender })
.select('id')
.single()

if (insertError) {
if (insertError.code === '23505') {
setError('Username already taken, try another')
} else {
setError('Failed to create account, please try again')
}
setLoading(false)
return
}

await supabase.from('balances').insert({
user_id: newUser.id,
gold: 100,
hvst: 0,
})

router.push('/farm')
}

if (!ready) return null

// Tiap frame = 1254/4 = 313.5px wide, 1254px tall
// Kita tampil frame pertama (menghadap depan) dengan object-position
const FRAME_WIDTH = 1254 / 4
return (
<main className="min-h-screen bg-green-950 flex flex-col items-center justify-center p-4">
<div className="bg-green-900 rounded-2xl p-8 w-full max-w-md space-y-6">
<h1 className="text-3xl font-bold text-green-300 text-center">Create Your Farmer</h1>

{/* Gender */}
<div className="space-y-2">
<p className="text-green-400 font-medium">Choose Gender</p>
<div className="grid grid-cols-2 gap-3">
{(['male', 'female'] as const).map((g) => (
<button
key={g}
onClick={() => setGender(g)}
className={`py-4 rounded-xl font-semibold transition-colors flex flex-col items-center gap-2 ${
gender === g
? 'bg-green-500 text-white ring-2 ring-green-300'
: 'bg-green-800 text-green-300 hover:bg-green-700'
}`}
>
{/* Sprite preview — crop frame pertama (menghadap depan) */}
<div
style={{
width: '80px',
height: '80px',
overflow: 'hidden',
imageRendering: 'pixelated',
position: 'relative',
}}
>
<img
src={`/assets/characters/${g}.png`}
alt={g}
style={{
position: 'absolute',
top: '0',
left: '0',
width: '320px',
height: '320px',
objectFit: 'none',
objectPosition: '0 0',
imageRendering: 'pixelated',
}}
/>
</div>
<span className="capitalize">{g}</span>
</button>
))}
</div>
</div>

{/* Username */}
<div className="space-y-2">
<p className="text-green-400 font-medium">Farmer Name</p>
<input
type="text"
value={username}
onChange={(e) => setUsername(e.target.value)}
placeholder="Enter your farmer name..."
maxLength={20}
className="w-full bg-green-800 text-green-100 placeholder-green-600 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-green-500"
/>
<p className="text-green-600 text-sm">{username.length}/20</p>
</div>

{error && <p className="text-red-400 text-sm">{error}</p>}

<button
onClick={handleSubmit}
disabled={loading}
className="w-full py-4 bg-green-500 hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold rounded-xl text-lg transition-colors"
>
{loading ? 'Creating...' : 'Start Farming →'}
</button>
</div>
</main>
)
}
