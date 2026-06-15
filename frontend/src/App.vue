<template>
  <div class="min-h-screen bg-green-800 text-white p-4">
    <!-- 标题 -->
    <h1 class="text-2xl font-bold text-center mb-6">🎰 德州扑克</h1>
    
    <!-- 调试信息 -->
    <div class="bg-black/30 p-3 rounded mb-4 text-sm">
      <p>API地址: {{ API_BASE_URL }}</p>
      <p>页面状态: 已加载 ✓</p>
    </div>
    
    <!-- 大厅视图 -->
    <div v-if="!room">
      <h2 class="text-xl mb-4">游戏大厅</h2>
      
      <!-- 创建房间按钮 -->
      <button 
        @click="createRoom" 
        class="w-full bg-blue-600 hover:bg-blue-700 py-3 px-4 rounded-lg mb-4 font-bold"
      >
        🎮 创建新房间
      </button>
      
      <!-- 加入房间 -->
      <div class="bg-black/20 p-4 rounded-lg">
        <h3 class="mb-2">加入房间</h3>
        <input 
          v-model="roomIdInput" 
          type="text" 
          placeholder="输入房间号"
          class="w-full bg-white/10 border border-white/30 rounded px-3 py-2 mb-3 text-white"
        >
        <button 
          @click="joinRoom" 
          class="w-full bg-green-600 hover:bg-green-700 py-2 px-4 rounded font-bold"
        >
          加入房间
        </button>
      </div>
    </div>
    
    <!-- 房间视图 -->
    <div v-else>
      <h2 class="text-xl mb-4">房间: {{ room.id }}</h2>
      
      <!-- 玩家列表 -->
      <div class="bg-black/20 p-4 rounded-lg mb-4">
        <h3 class="mb-2">玩家列表</h3>
        <div v-for="player in room.players" :key="player.id" class="py-2 border-b border-white/10">
          {{ player.name }} - 筹码: {{ player.chips }}
        </div>
      </div>
      
      <!-- 刷新按钮 -->
      <button 
        @click="refreshRoom" 
        class="w-full bg-yellow-600 hover:bg-yellow-700 py-2 px-4 rounded font-bold mb-4"
      >
        🔄 刷新房间
      </button>
      
      <!-- 返回大厅 -->
      <button 
        @click="leaveRoom" 
        class="w-full bg-gray-600 hover:bg-gray-700 py-2 px-4 rounded font-bold"
      >
        返回大厅
      </button>
    </div>
    
    <!-- 日志 -->
    <div class="mt-6 bg-black/30 p-3 rounded text-xs">
      <h3 class="mb-2 font-bold">日志:</h3>
      <div v-for="(log, i) in logs" :key="i" class="py-1">{{ log }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// ===== 配置 - 修改为你的Worker域名！=====
const API_BASE_URL = 'https://your-worker.workers.dev'  // ⚠️ 这里是Worker域名！
// =====================================

const room = ref(null)
const roomIdInput = ref('')
const logs = ref([])

function addLog(msg) {
  console.log(msg)
  logs.value.unshift(new Date().toLocaleTimeString() + ' - ' + msg)
  if (logs.value.length > 10) logs.value.pop()
}

onMounted(() => {
  addLog('页面加载完成')
  addLog('API地址: ' + API_BASE_URL)
})

async function createRoom() {
  addLog('点击创建房间...')
  try {
    const res = await fetch(API_BASE_URL + '/api/room/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId: 1, userName: '玩家1' })
    })
    const data = await res.json()
    addLog('响应: ' + JSON.stringify(data))
    if (data.success) {
      room.value = data.room
      addLog('房间创建成功!')
    } else {
      addLog('失败: ' + data.error)
      alert('创建失败: ' + data.error)
    }
  } catch (e) {
    addLog('错误: ' + e.message)
    alert('网络错误: ' + e.message)
  }
}

async function joinRoom() {
  if (!roomIdInput.value) {
    alert('请输入房间号')
    return
  }
  addLog('点击加入房间: ' + roomIdInput.value)
  try {
    const res = await fetch(API_BASE_URL + '/api/room/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ roomId: roomIdInput.value.toUpperCase(), userId: 2, userName: '玩家2' })
    })
    const data = await res.json()
    addLog('响应: ' + JSON.stringify(data))
    if (data.success) {
      room.value = data.room
      addLog('加入成功!')
    } else {
      addLog('失败: ' + data.error)
      alert('加入失败: ' + data.error)
    }
  } catch (e) {
    addLog('错误: ' + e.message)
    alert('网络错误: ' + e.message)
  }
}

async function refreshRoom() {
  if (!room.value) return
  addLog('刷新房间...')
  try {
    const res = await fetch(API_BASE_URL + '/api/room/' + room.value.id)
    const data = await res.json()
    if (data.success) {
      room.value = data.room
      addLog('刷新成功')
    }
  } catch (e) {
    addLog('刷新错误: ' + e.message)
  }
}

function leaveRoom() {
  room.value = null
  addLog('返回大厅')
}
</script>
