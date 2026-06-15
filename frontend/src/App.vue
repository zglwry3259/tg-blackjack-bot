<script setup>
import { ref, onMounted, reactive, computed } from 'vue'

// ==================== 配置 ====================
// ⚠️ 重要：这里必须填你的Worker域名，不是Pages域名！
// 示例：'https://poker-bot.yourname.workers.dev'
const API_BASE_URL = 'https://game.ttyun.eu.org/';

console.log('=== App 启动 ===');
console.log('API Base URL:', API_BASE_URL);

// ==================== 状态 ====================
const roomIdInput = ref('');
const room = ref(null);
const view = ref('lobby'); // lobby, game
const errorMsg = ref('');

const gameState = reactive({
  roomId: null,
  phase: 'waiting',
  communityCards: [],
  pot: 0,
  currentBet: 0,
  currentPlayer: 1,
  players: [],
  myPlayerId: 1
})

// ==================== 计算属性 ====================
const phaseText = computed(() => ({
  waiting: '等待玩家', pre_flop: '翻牌前', flop: '翻牌',
  turn: '转牌', river: '河牌', showdown: '摊牌'
}[gameState.phase] || gameState.phase))

const myPlayer = computed(() => gameState.players.find(p => p.id === gameState.myPlayerId))
const otherPlayers = computed(() => gameState.players.filter(p => p.id !== gameState.myPlayerId))
const isRed = (card) => card.includes('♥') || card.includes('♦')

// ==================== API 调用 ====================
async function createRoom() {
  console.log('=== 点击创建房间 ===');
  errorMsg.value = '';
  
  try {
    const res = await fetch(`${API_BASE_URL}/api/room/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        userId: 1, 
        userName: '玩家1' 
      })
    });
    
    const data = await res.json();
    console.log('创建房间响应:', data);
    
    if (data.success) {
      room.value = data.room;
      gameState.roomId = data.room.id;
      gameState.players = data.room.players;
      alert('✅ 房间创建成功！\n房间号：' + data.room.id + '\n把房间号发给好友加入！');
    } else {
      errorMsg.value = data.error || '创建失败';
      alert('❌ 创建失败：' + errorMsg.value);
    }
  } catch (e) {
    console.error('创建房间错误:', e);
    errorMsg.value = '网络错误：' + e.message;
    alert('❌ 网络错误\n\n请检查：\n1. API_BASE_URL 是否为Worker域名\n2. Worker是否已部署\n3. CORS是否配置正确');
  }
}

async function joinRoom() {
  console.log('=== 点击加入房间 ===');
  errorMsg.value = '';
  
  if (!roomIdInput.value) {
    alert('请输入房间号');
    return;
  }
  
  try {
    const res = await fetch(`${API_BASE_URL}/api/room/join`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        roomId: roomIdInput.value.toUpperCase(), 
        userId: 2, 
        userName: '玩家2' 
      })
    });
    
    const data = await res.json();
    console.log('加入房间响应:', data);
    
    if (data.success) {
      room.value = data.room;
      gameState.roomId = data.room.id;
      gameState.players = data.room.players;
      gameState.myPlayerId = 2;
      alert('✅ 加入成功！');
    } else {
      errorMsg.value = data.error || '加入失败';
      alert('❌ 加入失败：' + errorMsg.value);
    }
  } catch (e) {
    console.error('加入房间错误:', e);
    errorMsg.value = '网络错误：' + e.message;
    alert('❌ 网络错误\n\n请检查：\n1. API_BASE_URL 是否为Worker域名\n2. Worker是否已部署\n3. CORS是否配置正确');
  }
}

async function refreshRoom() {
  if (!room.value) return;
  
  try {
    const res = await fetch(`${API_BASE_URL}/api/room/${room.value.id}`);
    const data = await res.json();
    if (data.success) {
      room.value = data.room;
      gameState.players = data.room.players;
      console.log('刷新房间成功，玩家数:', data.room.players.length);
    }
  } catch (e) {
    console.error('刷新房间错误:', e);
  }
}

function startGame() {
  view.value = 'game';
  // 初始化演示数据
  gameState.phase = 'pre_flop';
  gameState.pot = 30;
  gameState.currentBet = 20;
  gameState.communityCards = ['A♠', 'K♦', 'Q♣'];
  if (gameState.players.length > 0) {
    gameState.players[0].hand = ['A♠', 'K♠'];
    gameState.players[0].chips = 980;
    gameState.players[0].current_bet = 10;
  }
  if (gameState.players.length > 1) {
    gameState.players[1].hand = ['Q♥', 'J♥'];
    gameState.players[1].chips = 960;
    gameState.players[1].current_bet = 20;
  }
}

function backToLobby() {
  view.value = 'lobby';
}

// ==================== 生命周期 ====================
onMounted(() => {
  console.log('App mounted');
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.ready()
    window.Telegram.WebApp.expand()
  }
  
  // 自动刷新房间
  setInterval(refreshRoom, 3000);
})
</script>

<template>
  <div class="min-h-screen p-4 max-w-lg mx-auto">
    
    <!-- 大厅视图 -->
    <div v-if="view === 'lobby'">
      <header class="bg-black/30 backdrop-blur-sm py-6 px-4 rounded-xl mb-6 text-center">
        <h1 class="text-2xl font-bold text-poker-gold mb-2">🎰 德州扑克</h1>
        <p class="text-sm opacity-75">多人在线联机</p>
      </header>
      
      <!-- 错误提示 -->
      <div v-if="errorMsg" class="bg-red-500/20 border border-red-500 rounded-lg p-3 mb-4 text-red-300 text-sm">
        ❌ {{ errorMsg }}
      </div>
      
      <!-- 创建房间 -->
      <div class="bg-black/20 rounded-xl p-4 mb-4">
        <h3 class="font-bold mb-3 text-poker-gold">🏠 创建房间</h3>
        <button @click="createRoom" class="btn btn-success w-full">
          ➕ 创建新房间
        </button>
      </div>
      
      <!-- 加入房间 -->
      <div class="bg-black/20 rounded-xl p-4 mb-6">
        <h3 class="font-bold mb-3 text-poker-gold">🚪 加入房间</h3>
        <div class="flex gap-2">
          <input 
            v-model="roomIdInput" 
            type="text" 
            placeholder="输入房间号" 
            class="flex-1 bg-black/30 border border-white/20 rounded-lg px-4 py-3 text-white"
            maxlength="8"
          >
          <button @click="joinRoom" class="btn btn-primary">
            加入
          </button>
        </div>
      </div>
      
      <!-- 房间信息 -->
      <div v-if="room" class="bg-black/20 rounded-xl p-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold text-poker-gold">📋 房间信息</h3>
          <button @click="refreshRoom" class="text-sm text-poker-green">🔄 刷新</button>
        </div>
        
        <div class="space-y-2 mb-4">
          <div class="flex justify-between">
            <span class="opacity-75">房间号</span>
            <span class="font-mono font-bold">{{ room.id }}</span>
          </div>
          <div class="flex justify-between">
            <span class="opacity-75">状态</span>
            <span class="text-poker-green">等待玩家</span>
          </div>
          <div class="flex justify-between">
            <span class="opacity-75">玩家数</span>
            <span>{{ room.players.length }} / 6</span>
          </div>
        </div>
        
        <div class="mb-4">
          <div class="text-sm opacity-75 mb-2">玩家列表</div>
          <div class="space-y-2">
            <div v-for="player in room.players" :key="player.id" 
                 class="flex justify-between bg-black/20 rounded-lg px-3 py-2">
              <span>{{ player.name }}</span>
              <span class="text-poker-gold">💰 {{ player.chips }}</span>
            </div>
          </div>
        </div>
        
        <button @click="startGame" class="btn btn-primary w-full">
          🎮 开始游戏
        </button>
      </div>
      
      <!-- 配置提示 -->
      <div class="mt-6 bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4 text-sm">
        <div class="font-bold text-yellow-400 mb-2">⚠️ 重要配置提示</div>
        <div class="opacity-75 space-y-1">
          <p>1. 打开 <code class="bg-black/30 px-1 rounded">frontend/src/App.vue</code></p>
          <p>2. 修改 <code class="bg-black/30 px-1 rounded">API_BASE_URL</code> 为你的Worker域名</p>
          <p>3. 重新部署Pages</p>
        </div>
      </div>
    </div>
    
    <!-- 游戏视图 -->
    <div v-else>
      <header class="bg-black/30 backdrop-blur-sm py-4 px-4 rounded-xl mb-4">
        <div class="flex items-center justify-between">
          <button @click="backToLobby" class="text-sm opacity-75">← 返回</button>
          <h1 class="text-xl font-bold text-poker-gold">🎰 德州扑克</h1>
          <div class="text-sm opacity-75">房间: {{ gameState.roomId }}</div>
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
            <div class="font-bold text-sm">{{ player.name }}</div>
            <div class="text-poker-gold text-sm">💰 {{ player.chips }}</div>
          </div>
          <div class="flex justify-center gap-1 mb-2">
            <div class="card card-back scale-75"><span class="text-white text-xl">🎴</span></div>
            <div class="card card-back scale-75"><span class="text-white text-xl">🎴</span></div>
          </div>
          <div class="text-center text-xs opacity-75">下注: {{ player.current_bet || 0 }}</div>
        </div>
      </div>
      
      <div class="bg-black/20 rounded-3xl p-6 mb-6 border-2 border-poker-gold/30">
        <div class="flex justify-center gap-2">
          <div v-for="(card, i) in gameState.communityCards" :key="i"
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
            <div class="font-bold">{{ myPlayer?.name }}</div>
            <div class="text-poker-gold">💰 {{ myPlayer?.chips }}</div>
          </div>
          <div class="text-right">
            <div class="text-sm opacity-75">当前下注</div>
            <div class="font-bold">{{ myPlayer?.current_bet || 0 }}</div>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-2 gap-3">
        <button class="btn btn-danger">弃牌 (Fold)</button>
        <button class="btn btn-secondary">跟注 {{ gameState.currentBet }} (Call)</button>
        <button class="btn btn-primary col-span-2">加注 (Raise)</button>
      </div>
      <button class="btn btn-success w-full mt-3">全押 ALL-IN ({{ myPlayer?.chips }})</button>
    </div>
    
  </div>
</template>
