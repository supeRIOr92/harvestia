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
// Cek apakah user sudah punya akun
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
if (!gender) return setError('Pilih gender dulu')
if (!username.trim()) return setError('Nama karakter tidak boleh kosong')
if (username.trim().length < 3) return setError('Nama minimal 3 karakter')
if (username.trim().length > 20) return setError('Nama maksimal 20 karakter')

const wallet = user?.wallet?.address
if (!wallet) return setError('Wallet tidak ditemukan')

setLoading(true)
setError('')

const { error: insertError } = await supabase.from('users').insert({
wallet_address: wallet,
username: username.trim(),
gender,
})

if (insertError) {
if (insertError.code === '23505') {
setError('Username sudah dipakai, coba yang lain')
} else {
setError('Gagal membuat akun, coba lagi')
}
setLoading(false)
return
}

// Buat balance awal
await supabase.from('balances').insert({
user_id: (await supabase.from('users').select('id').eq('wallet_address', wallet).single()).data?.id,
gold: 100,
hvst: 0,
})

router.push('/farm')
}

if (!ready) return null

return (
<main className="min-h-screen bg-green-950 flex flex-col items-center justify-center p-4">
<div className="bg-green-900 rounded-2xl p-8 w-full max-w-md space-y-6">
<h1 className="text-3xl font-bold text-green-300 text-center">Create Your Farmer</h1>

{/* Gender */}
<div className="space-y-2">
<p className="text-green-400 font-medium">Choose Gender</p>
<div className="grid grid-cols-2 gap-3">
<button
onClick={() => setGender('male')}
className={`py-4 rounded-xl font-semibold transition-colors ${
gender === 'male'
? 'bg-green-500 text-white'
: 'bg-green-800 text-green-300 hover:bg-green-700'
}`}
>
👨 Male
</button>
<button
onClick={() => setGender('female')}
className={`py-4 rounded-xl font-semibold transition-colors ${
gender === 'female'
? 'bg-green-500 text-white'
: 'bg-green-800 text-green-300 hover:bg-green-700'
}`}
>
👩 Female
</button>
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

{/* Error */}
{error && (
<p className="text-red-400 text-sm">{error}</p>
)}

{/* Submit */}
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
