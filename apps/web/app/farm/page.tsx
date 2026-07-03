'use client'

import { useEffect, useRef } from 'react'
import { usePrivy } from '@privy-io/react-auth'
import { useRouter } from 'next/navigation'

export default function FarmPage() {
const { ready, authenticated } = usePrivy()
const router = useRouter()
const gameRef = useRef<HTMLDivElement>(null)

useEffect(() => {
if (ready && !authenticated) {
router.push('/')
}
}, [ready, authenticated, router])

useEffect(() => {
if (!ready || !authenticated) return

let game: any

const initPhaser = async () => {
const Phaser = (await import('phaser')).default

const TILE_SIZE = 64
const GRID_SIZE = 9
const MAP_SIZE = TILE_SIZE * GRID_SIZE

class FarmScene extends Phaser.Scene {
private player!: Phaser.GameObjects.Image
private cursors!: Phaser.Types.Input.Keyboard.CursorKeys
private wasd!: { up: Phaser.Input.Keyboard.Key; down: Phaser.Input.Keyboard.Key; left: Phaser.Input.Keyboard.Key; right: Phaser.Input.Keyboard.Key }
private playerSpeed = 180
private playerDir = 'down'

constructor() {
super({ key: 'FarmScene' })
}

preload() {
// Ground tiles
this.load.image('grassy', '/assets/characters-resized/grassy.png')
this.load.image('soil', '/assets/characters-resized/soil.png')

// Character spritesheet — 4 frames horizontal
this.load.spritesheet('player_male', '/assets/characters-resized/male.png', {
frameWidth: 32, // 125px resized to ~32px
frameHeight: 64,
})
}

create() {
const offsetX = 100
const offsetY = 80

// Draw grass background
for (let y = -2; y < GRID_SIZE + 2; y++) {
for (let x = -2; x < GRID_SIZE + 2; x++) {
this.add.image(
offsetX + x * TILE_SIZE + TILE_SIZE / 2,
offsetY + y * TILE_SIZE + TILE_SIZE / 2,
'grassy'
).setDisplaySize(TILE_SIZE, TILE_SIZE)
}
}

// Draw farm plots (soil)
for (let y = 0; y < GRID_SIZE; y++) {
for (let x = 0; x < GRID_SIZE; x++) {
this.add.image(
offsetX + x * TILE_SIZE + TILE_SIZE / 2,
offsetY + y * TILE_SIZE + TILE_SIZE / 2,
'soil'
).setDisplaySize(TILE_SIZE, TILE_SIZE)
}
}

// Player
this.player = this.add.image(
offsetX + TILE_SIZE * 4,
offsetY + TILE_SIZE * 4,
'player_male'
).setDisplaySize(48, 64)

// Camera follow player
this.cameras.main.startFollow(this.player)
this.cameras.main.setZoom(1.5)

// Input
this.cursors = this.input.keyboard!.createCursorKeys()
this.wasd = {
up: this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.W),
down: this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.S),
left: this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.A),
right: this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.D),
}
}

update() {
const speed = this.playerSpeed
let vx = 0
let vy = 0

if (this.wasd.left.isDown || this.cursors.left.isDown) {
vx = -speed
this.playerDir = 'left'
} else if (this.wasd.right.isDown || this.cursors.right.isDown) {
vx = speed
this.playerDir = 'right'
}

if (this.wasd.up.isDown || this.cursors.up.isDown) {
vy = -speed
this.playerDir = 'up'
} else if (this.wasd.down.isDown || this.cursors.down.isDown) {
vy = speed
this.playerDir = 'down'
}

// Move player (manual position update since using Image not Physics)
const dt = this.game.loop.delta / 1000
this.player.x += vx * dt
this.player.y += vy * dt

// Swap frame based on direction
// Frame 0=down, 1=up, 2=left, 3=right
const frameMap: Record<string, number> = { down: 0, up: 1, left: 2, right: 3 }
// We use setTexture crop since it's a plain Image, not sprite
// Will upgrade to sprite in next step
}
}

game = new Phaser.Game({
type: Phaser.AUTO,
width: window.innerWidth,
height: window.innerHeight,
backgroundColor: '#2d5a27',
parent: gameRef.current!,
scene: FarmScene,
})
}

initPhaser()

return () => {
game?.destroy(true)
}
}, [ready, authenticated])

if (!ready) return null

return (
<div
ref={gameRef}
style={{ width: '100vw', height: '100vh', overflow: 'hidden' }}
/>
)
}