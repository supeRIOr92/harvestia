import { Controller, Get, Post, Body, Param } from '@nestjs/common'
import { UsersService } from './users.service'

@Controller('users')
export class UsersController {
constructor(private usersService: UsersService) {}

@Get(':wallet')
async getUser(@Param('wallet') wallet: string) {
const user = await this.usersService.findByWallet(wallet)
return { user }
}

@Post()
async createUser(
@Body() body: { walletAddress: string; username: string; gender: string },
) {
const taken = await this.usersService.isUsernameTaken(body.username)
if (taken) {
return { error: 'Username already taken' }
}
const user = await this.usersService.create(
body.walletAddress,
body.username,
body.gender,
)
return { user }
}
}
