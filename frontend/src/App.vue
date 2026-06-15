<script setup>
import { ref, onMounted, reactive, computed } from 'vue'

const gameState = reactive({
  roomId: null,
  phase: 'waiting',
  communityCards: [],
  pot: 30,
  currentBet: 20,
  currentPlayer: 2,
  players: [
    { id: 1, username: 'Player1', first_name: '玩家1', chips: 980, current_bet: 10, is_folded: false, hand: ['A♠', 'K♠'] },
    { id: 2, username: 'You', first_name: '你', chips: 960, current_bet: 20, is_folded: false, hand: ['Q♥', 'J♥'] },
    { id: 3, username: 'Player3', first_name: '玩家3', chips: 1000, current_bet: 0, is_folded: false, hand: [] }
  ],
  myPlayerId: 2
})

const phaseText = computed(() => ({
  waiting: '等待玩家', pre_flop: '翻牌前', flop: '翻牌',
  turn: '转牌', river: '河牌', showdown: '摊牌'
}[gameState.phase] || gameState.phase))

const myPlayer = computed(() => gameState.players.find(p => p.id === gameState.myPlayerId))
const otherPlayers = computed(() => gameState.players.filter(p => p.id !== gameState.myPlayerId))

const isRed = (card) => card.includes('♥') || card.includes('♦')

onMounted(() => {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.ready()
    window.Telegram.WebApp.expand()
  }
})
</script>

<template>
  <div class="min-h-screen p-4 max-w-lg mx-auto">
    <header class="bg-black/30 backdrop-blur-sm py-4 px-4 rounded-xl mb-4">
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-bold text-poker-gold">🎰 德州扑克</h1>
        <div class="text-sm opacity-75">房间: DEMO</div>
      </div>
    </header>

    <div class="flex justify-between items-center mb-4 px-2">
      <div class="text-sm opacity-75">阶段: {{ phaseText }}</div>
      <div class="pot-display">💰 底池: {{ gameState.pot }}</div>
    </div>

    <div class="grid grid-cols-2 gap-3 mb-6">
      <div v-for="player in otherPlayers" :key="player.id" 
           class="player-seat" :class="{ active: player.id === gameState.currentPlayer, folded: player.is_folded }">
        <div class="flex justify-between mb-2">
          <div class="font-bold text-sm">{{ player.first_name }}</div>
          <div class="text-poker-gold text-sm">💰 {{ player.chips }}</div>
        </div>
        <div class="flex justify-center gap-1 mb-2">
          <div class="card card-back scale-75"><span class="text-white text-xl">🎴</span></div>
          <div class="card card-back scale-75"><span class="text-white text-xl">🎴</span></div>
        </div>
        <div class="text-center text-xs opacity-75">下注: {{ player.current_bet }}</div>
      </div>
    </div>

    <div class="bg-black/20 rounded-3xl p-6 mb-6 border-2 border-poker-gold/30">
      <div class="flex justify-center gap-2">
        <div v-for="(card, i) in ['A♠', 'K♦', 'Q♣']" :key="i"
             class="card" :class="{ 'card-red': isRed(card), 'card-black': !isRed(card) }">
          <div class="flex flex-col items-center">
            <span>{{ card.slice(0, -1) }}</span>
            <span>{{ card.slice(-1) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="mb-6">
      <div class="text-sm mb-2 opacity-75">我的手牌</div>
      <div class="flex justify-center gap-3">
        <div v-for="(card, i) in myPlayer?.hand || []" :key="i"
             class="card" :class="{ 'card-red': isRed(card), 'card-black': !isRed(card) }">
          <div class="flex flex-col items-center">
            <span class="text-lg">{{ card.slice(0, -1) }}</span>
            <span class="text-xl">{{ card.slice(-1) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-black/30 rounded-xl p-4 mb-6">
      <div class="flex justify-between">
        <div>
          <div class="font-bold">{{ myPlayer?.first_name }}</div>
          <div class="text-poker-gold">💰 {{ myPlayer?.chips }}</div>
        </div>
        <div class="text-right">
          <div class="text-sm opacity-75">当前下注</div>
          <div class="font-bold">{{ myPlayer?.current_bet }}</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-3">
      <button class="btn btn-danger">弃牌 (Fold)</button>
      <button class="btn btn-secondary">跟注 20 (Call)</button>
      <button class="btn btn-primary col-span-2">加注 (Raise)</button>
    </div>
    <button class="btn btn-success w-full mt-3">全押 ALL-IN ({{ myPlayer?.chips }})</button>
  </div>
</template>
