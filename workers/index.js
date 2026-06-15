// 第一行就执行，确保能在日志中看到
console.log('=== WORKER SCRIPT LOADED ===');

// 给所有响应添加CORS头
function addCorsHeaders(headers) {
  headers.set('Access-Control-Allow-Origin', '*');
  headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  return headers;
}

// 生成房间ID
function generateRoomId() {
  return Math.random().toString(36).substring(2, 8).toUpperCase();
}

// 发送Telegram消息
async function sendTelegramMessage(token, chatId, text) {
  console.log('=== SENDING TELEGRAM MESSAGE ===');
  console.log('Chat ID:', chatId);
  console.log('Text:', text);
  console.log('Token first 10 chars:', token.substring(0, 10) + '...');
  
  try {
    const response = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_id: chatId,
        text: text
      })
    });
    
    const result = await response.json();
    console.log('Telegram API response status:', response.status);
    console.log('Telegram API result:', JSON.stringify(result));
    
    if (!result.ok) {
      console.error('Telegram API error:', result.description);
    }
    
    return result;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

export default {
  async fetch(request, env, ctx) {
    // CORS 预检请求处理 - 最优先
    if (request.method === 'OPTIONS') {
      console.log('CORS Preflight request');
      return new Response(null, {
        headers: addCorsHeaders(new Headers()),
      });
    }
    
    // 第一步：打印请求信息
    console.log('=== REQUEST RECEIVED ===');
    console.log('Method:', request.method);
    console.log('URL:', request.url);
    console.log('Headers:', Object.fromEntries(request.headers));
    
    const url = new URL(request.url);
    
    try {
      // 健康检查
      if (url.pathname === '/' || url.pathname === '') {
        console.log('Health check');
        return new Response('Poker Bot is running!', {
          headers: addCorsHeaders(new Headers())
        });
      }
      
      // 测试路由 - 诊断
      if (url.pathname === '/test') {
        console.log('Test route');
        return new Response(JSON.stringify({
          tokenExists: !!env.TELEGRAM_BOT_TOKEN,
          tokenFirst10: env.TELEGRAM_BOT_TOKEN ? env.TELEGRAM_BOT_TOKEN.substring(0, 10) + '...' : 'NOT SET',
          secretExists: !!env.WEBHOOK_SECRET,
          webAppUrl: env.TELEGRAM_WEB_APP_URL || 'NOT SET',
          kvExists: !!env.ROOMS
        }, null, 2), {
          headers: addCorsHeaders(new Headers({ 'Content-Type': 'application/json' }))
        });
      }
      
      // ==================== API 路由 ====================
      
      // API: 创建房间
      if (url.pathname === '/api/room/create' && request.method === 'POST') {
        console.log('API: 创建房间');
        const body = JSON.parse(await request.text());
        const roomId = generateRoomId();
        const room = {
          id: roomId,
          creator: body.userId,
          creatorName: body.userName,
          players: [{ id: body.userId, name: body.userName, chips: 1000 }],
          status: 'waiting',
          createdAt: Date.now()
        };
        await env.ROOMS.put(`room:${roomId}`, JSON.stringify(room));
        console.log('房间创建成功:', roomId);
        return new Response(JSON.stringify({ success: true, room }), {
          headers: addCorsHeaders(new Headers({ 'Content-Type': 'application/json' }))
        });
      }
      
      // API: 加入房间
      if (url.pathname === '/api/room/join' && request.method === 'POST') {
        console.log('API: 加入房间');
        const body = JSON.parse(await request.text());
        const roomData = await env.ROOMS.get(`room:${body.roomId}`);
        if (!roomData) {
          console.log('房间不存在:', body.roomId);
          return new Response(JSON.stringify({ success: false, error: '房间不存在' }), {
            headers: addCorsHeaders(new Headers({ 'Content-Type': 'application/json' }))
          });
        }
        const room = JSON.parse(roomData);
        room.players.push({ id: body.userId, name: body.userName, chips: 1000 });
        await env.ROOMS.put(`room:${room.id}`, JSON.stringify(room));
        console.log('加入房间成功:', body.roomId);
        return new Response(JSON.stringify({ success: true, room }), {
          headers: addCorsHeaders(new Headers({ 'Content-Type': 'application/json' }))
        });
      }
      
      // API: 获取房间状态
      if (url.pathname.startsWith('/api/room/') && request.method === 'GET') {
        const roomId = url.pathname.split('/').pop();
        console.log('API: 获取房间', roomId);
        const roomData = await env.ROOMS.get(`room:${roomId}`);
        if (!roomData) {
          return new Response(JSON.stringify({ success: false, error: '房间不存在' }), {
            headers: addCorsHeaders(new Headers({ 'Content-Type': 'application/json' }))
          });
        }
        return new Response(JSON.stringify({ success: true, room: JSON.parse(roomData) }), {
          headers: addCorsHeaders(new Headers({ 'Content-Type': 'application/json' }))
        });
      }
      
      // ==================== Webhook 处理 ====================
      
      // Webhook处理
      if (url.pathname === '/webhook' && request.method === 'POST') {
        console.log('=== WEBHOOK PROCESSING START ===');
        
        // 克隆请求体（避免读取一次后无法再读）
        const requestBody = await request.text();
        console.log('Request body:', requestBody);
        
        let update;
        try {
          update = JSON.parse(requestBody);
          console.log('Parsed update:', JSON.stringify(update));
        } catch (e) {
          console.error('JSON parse error:', e);
          return new Response('Invalid JSON', { status: 400 });
        }
        
        // 处理消息
        if (update.message && update.message.text) {
          const chatId = update.message.chat.id;
          const text = update.message.text;
          console.log('Message received:', text, 'from chat:', chatId);
          
          // 响应 /start
          if (text.startsWith('/start')) {
            console.log('Handling /start command');
            await sendTelegramMessage(env.TELEGRAM_BOT_TOKEN, chatId, 
              '🎰 欢迎来到德州扑克游戏！发送 /newgame 创建房间'
            );
          }
          // 响应 /newgame
          else if (text.startsWith('/newgame')) {
            console.log('Handling /newgame command');
            await sendTelegramMessage(env.TELEGRAM_BOT_TOKEN, chatId, 
              '✅ 房间已创建！点击下方按钮进入游戏'
            );
          }
          // 响应其他消息
          else {
            console.log('Handling other message');
            await sendTelegramMessage(env.TELEGRAM_BOT_TOKEN, chatId, 
              '收到消息：' + text
            );
          }
        }
        
        console.log('=== WEBHOOK PROCESSING COMPLETE ===');
        return new Response('OK', {
          headers: addCorsHeaders(new Headers())
        });
      }
      
      console.log('Route not found:', url.pathname);
      return new Response('Not Found', { 
        status: 404,
        headers: addCorsHeaders(new Headers())
      });
      
    } catch (error) {
      console.error('=== GLOBAL ERROR ===');
      console.error('Error:', error);
      console.error('Error stack:', error.stack);
      return new Response('Error: ' + error.message, { 
        status: 500,
        headers: addCorsHeaders(new Headers())
      });
    }
  }
};
