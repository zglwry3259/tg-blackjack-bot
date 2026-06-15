/**
 * Telegram Poker Bot - Cloudflare Worker
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok' }), {
        headers: { 'Content-Type': 'application/json' }
      })
    }
    
    if (url.pathname === '/webhook') {
      return await handleWebhook(request, env)
    }
    
    if (url.pathname.startsWith('/api/')) {
      return await handleAPI(request, env)
    }
    
    return new Response('Telegram Poker Bot Worker', { status: 200 })
  }
}

async function handleWebhook(request, env) {
  const secret = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
  if (secret !== env.WEBHOOK_SECRET) {
    return new Response('Unauthorized', { status: 401 })
  }
  
  const update = await request.json()
  
  if (update.message) {
    await handleMessage(update.message, env)
  }
  
  if (update.callback_query) {
    await handleCallback(update.callback_query, env)
  }
  
  return new Response('OK')
}

async function handleMessage(message, env) {
  const chatId = message.chat.id
  const text = message.text || ''
  const user = message.from
  
  if (text.startsWith('/')) {
    const cmd = text.slice(1).split(' ')[0]
    
    if (cmd === 'start' || cmd === 'newgame') {
      await sendMessage(chatId, '🎮 游戏房间已创建！\n\n点击下方按钮开始游戏', {
        inline_keyboard: [[{
          text: '🎴 打开游戏',
          web_app: { url: env.TELEGRAM_WEB_APP_URL }
        }]]
      }, env)
    } else if (cmd === 'rules') {
      await sendMessage(chatId, '📖 德州扑克规则\n\n1. 每人2张底牌\n2. 5张公共牌\n3. 最好的5张牌获胜\n\n牌型: 皇家同花顺 > 同花顺 > 四条 > 葫芦 > 同花 > 顺子 > 三条 > 两对 > 一对 > 高牌', null, env)
    } else {
      await sendMessage(chatId, '🎰 德州扑克 Bot\n\n命令:\n/newgame - 创建游戏\n/rules - 游戏规则', null, env)
    }
  }
}

async function handleCallback(callback, env) {
  await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/answerCallbackQuery`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ callback_query_id: callback.id })
  })
}

async function sendMessage(chatId, text, replyMarkup, env) {
  const body = { chat_id: chatId, text, parse_mode: 'Markdown' }
  if (replyMarkup) body.reply_markup = replyMarkup
  
  await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
}

async function handleAPI(request, env) {
  const url = new URL(request.url)
  
  if (url.pathname === '/api/rooms' && request.method === 'POST') {
    const data = await request.json()
    const roomId = Math.random().toString(36).slice(2, 10).toUpperCase()
    await env.ROOMS.put(`room:${roomId}`, JSON.stringify(data))
    return new Response(JSON.stringify({ roomId }), {
      headers: { 'Content-Type': 'application/json' }
    })
  }
  
  if (url.pathname.startsWith('/api/rooms/')) {
    const roomId = url.pathname.split('/').pop()
    const room = await env.ROOMS.get(`room:${roomId}`)
    if (!room) return new Response('Not Found', { status: 404 })
    return new Response(room, {
      headers: { 'Content-Type': 'application/json' }
    })
  }
  
  return new Response('Not Found', { status: 404 })
}
