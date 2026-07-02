import { Injectable } from '@nestjs/common'
import { SupabaseService } from '../supabase/supabase.service'

@Injectable()
export class UsersService {
constructor(private supabase: SupabaseService) {}

async findByWallet(walletAddress: string) {
const { data, error } = await this.supabase
.getClient()
.from('users')
.select('*, balances(*)')
.eq('wallet_address', walletAddress)
.single()

if (error) return null
return data
}

async create(walletAddress: string, username: string, gender: string) {
const { data: user, error } = await this.supabase
.getClient()
.from('users')
.insert({ wallet_address: walletAddress, username, gender })
.select()
.single()

if (error) throw new Error(error.message)

await this.supabase.getClient().from('balances').insert({
user_id: user.id,
gold: 100,
hvst: 0,
})

return user
}

async isUsernameTaken(username: string) {
const { data } = await this.supabase
.getClient()
.from('users')
.select('id')
.eq('username', username)
.single()

return !!data
}
}
