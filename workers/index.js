export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // 调试日志
    console.log('收到请求:', request.method, url.pathname);
    
    // 测试路由 - 验证Worker运行和环境变量状态
    if (url.pathname === '/test') {
      return new Response(JSON.stringify({
        status: 'ok',
        message: 'Worker is running!',
        env: {
          hasToken: !!env.TELEGRAM_BOT_TOKEN,
          hasSecret: !!env.WEBHOOK_SECRET,
          hasWebAppUrl: !!env.TELEGRAM_WEB_APP_URL,
          hasKV: !!env.ROOMS
        }
      }, null, 2), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // 健康检查
    if (url.pathname === '/' || url.pathname === '') {
      return new Response('Poker Bot is running! Visit /test for details');
    }
    
    // Webhook处理
    if (url.pathname === '/webhook' && request.method === 'POST') {
      try {
        // 验证Webhook secret
        const secretHeader = request.headers.get('X-Telegram-Bot-Api-Secret-Token');
        console.log('Webhook Secret Header:', secretHeader);
        console.log('Expected Secret:', env.WEBHOOK_SECRET);
        
        if (secretHeader !== env.WEBHOOK_SECRET) {
          console.log('Webhook Secret 不匹配！');
          return new Response('Unauthorized', { status: 401 });
        }
        
        // 解析请求体
        const update = await request.json();
        console.log('收到Update:', JSON.stringify(update, null, 2));
        
        // 处理消息
        if (update.message) {
          const message = update.message;
          const chatId = message.chat.id;
          const text = message.text || '';
          const userId = message.from.id;
          const username = message.from.username || message.from.first_name;
          
          console.log('收到消息:', chatId, text, '来自:', username);
          
          // 处理命令
          if (text === '/start') {
            console.log('处理 /start 命令');
            await sendMessage(env.TELEGRAM_BOT_TOKEN, chatId, 
              `🎰 欢迎来到德州扑克游戏！\n\n` +
              `命令：\n` +
              `/newgame - 创建新游戏\n` +
              `/rules - 游戏规则\n` +
              `/help - 帮助`
            );
          }
          else if (text === '/newgame') {
            console.log('处理 /newgame 命令');
            const roomId = generateRoomId();
            await env.ROOMS.put(`room:${roomId}`, JSON.stringify({
              id: roomId,
              creator: userId,
              players: [{ id: userId, name: username }],
              status: 'waiting',
              createdAt: Date.now()
            }));
            
            const inviteLink = `${env.TELEGRAM_WEB_APP_URL}?room=${roomId}`;
            await sendMessage(env.TELEGRAM_BOT_TOKEN, chatId, 
              `✅ 游戏房间已创建！\n\n` +
              `房间号: ${roomId}\n` +
              `邀请链接: ${inviteLink}\n\n` +
              `点击下方按钮开始游戏：`,
              {
                inline_keyboard: [[{
                  text: '🎮 开始游戏',
                  web_app: { url: inviteLink }
                }]]
              }
            );
          }
          else if (text === '/rules') {
            await sendMessage(env.TELEGRAM_BOT_TOKEN, chatId, 
              `📖 德州扑克规则：\n\n` +
              `1. 每人发2张底牌\n` +
              `2. 分3轮发公共牌（3+1+1）\n` +
              `3. 每轮可下注/跟注/弃牌\n` +
              `4. 用7张牌选5张组成最大牌型\n\n` +
              `牌型大小：同花顺 > 四条 > 葫芦 > 同花 > 顺子 > 三条 > 两对 > 一对 > 高牌`
            );
          }
          else if (text === '/help') {
            await sendMessage(env.TELEGRAM_BOT_TOKEN, chatId, 
              `❓ 帮助：\n\n` +
              `/newgame - 创建新游戏房间\n` +
              `创建后分享邀请链接给好友\n` +
              `点击Web App按钮进入游戏界面\n` +
              `支持2-6人联机对战`
            );
          }
        }
        
        return new Response('OK');
      } catch (error) {
        console.error('处理Webhook错误:', error);
        return new Response('Error: ' + error.message, { status: 500 });
      }
    }
    
    return new Response('Not Found', { status: 404 });
  }
};

// 发送消息到Telegram
async function sendMessage(token, chatId, text, replyMarkup = null) {
  console.log('发送消息到:', chatId, '内容:', text.substring(0, 50));
  
  const body = {
    chat_id: chatId,
    text: text,
    parse_mode: 'HTML'
  };
  
  if (replyMarkup) {
    body.reply_markup = replyMarkup;
  }
  
  const response = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
  
  const result = await response.json();
  console.log('Telegram API响应:', result);
  
  if (!result.ok) {
    console.error('发送消息失败:', result);
  }
  
  return result;
}

// 生成房间ID
function generateRoomId() {
  return Math.random().toString(36).substring(2, 8).toUpperCase();
}
