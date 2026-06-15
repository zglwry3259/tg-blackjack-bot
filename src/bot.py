#!/usr/bin/env python3
"""
Telegram 德州扑克 Bot 主入口
"""
import os
import asyncio
import logging
import uuid
import time
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEB_APP_URL = os.getenv('TELEGRAM_WEB_APP_URL', 'https://your-project.pages.dev')

# 全局房间存储
rooms = {}
player_to_room = {}


def generate_room_id():
    return str(uuid.uuid4())[:8].upper()


def generate_invite_code():
    return str(uuid.uuid4())[:6].upper()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    user = update.effective_user
    
    # 检查邀请参数
    if context.args:
        invite_code = context.args[0]
        for room_id, room in rooms.items():
            if room['invite_code'] == invite_code.upper():
                success = join_room_internal(room_id, user.id, user.username or user.first_name, user.first_name)
                if success:
                    await update.message.reply_text(
                        f"✅ 成功加入房间！\n房间号: {room_id}\n当前玩家: {len(room['players'])}/10"
                    )
                    await show_game_buttons(update, context, room_id)
                    return
    
    welcome_text = (
        f"🎰 欢迎来到德州扑克 Bot, {user.first_name}!\n\n"
        f"📋 可用命令:\n"
        f"/newgame - 创建新游戏房间\n"
        f"/join [房间号] - 加入房间\n"
        f"/rules - 查看游戏规则\n"
        f"/help - 查看帮助"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 创建房间", callback_data="create_room"),
            InlineKeyboardButton("📖 游戏规则", callback_data="show_rules")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


def join_room_internal(room_id, user_id, username, first_name):
    """内部加入房间"""
    if room_id not in rooms:
        return False
    
    room = rooms[room_id]
    if len(room['players']) >= 10:
        return False
    
    # 检查是否已在房间
    for p in room['players']:
        if p['id'] == user_id:
            return True
    
    # 从其他房间移除
    if user_id in player_to_room and player_to_room[user_id] in rooms:
        old_room = rooms[player_to_room[user_id]]
        old_room['players'] = [p for p in old_room['players'] if p['id'] != user_id]
    
    room['players'].append({
        'id': user_id,
        'username': username,
        'first_name': first_name,
        'chips': 1000,
        'current_bet': 0,
        'is_folded': False
    })
    player_to_room[user_id] = room_id
    return True


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """创建新游戏"""
    user = update.effective_user
    chat = update.effective_chat
    
    # 检查是否已在房间
    if user.id in player_to_room:
        await update.message.reply_text("⚠️ 你已在房间中，请先 /leave 离开")
        return
    
    room_id = generate_room_id()
    invite_code = generate_invite_code()
    
    rooms[room_id] = {
        'id': room_id,
        'invite_code': invite_code,
        'created_by': user.id,
        'chat_id': chat.id,
        'players': [{
            'id': user.id,
            'username': user.username or user.first_name,
            'first_name': user.first_name,
            'chips': 1000,
            'current_bet': 0,
            'is_folded': False
        }],
        'phase': 'waiting',
        'created_at': time.time()
    }
    player_to_room[user.id] = room_id
    
    invite_link = f"https://t.me/{context.bot.username}?start={invite_code}"
    
    text = (
        f"🎮 游戏房间创建成功！\n\n"
        f"房间号: `{room_id}`\n"
        f"邀请码: `{invite_code}`\n"
        f"邀请链接: {invite_link}\n\n"
        f"当前玩家: 1/10\n等待其他玩家加入..."
    )
    
    await show_game_buttons(update, context, room_id, text)


async def show_game_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, room_id, text=None):
    """显示游戏按钮"""
    if room_id not in rooms:
        return
    
    room = rooms[room_id]
    if not text:
        text = f"🎮 房间 {room_id}\n当前玩家: {len(room['players'])}/10"
    
    web_app_url = f"{WEB_APP_URL}?room_id={room_id}"
    
    keyboard = [
        [InlineKeyboardButton("🎴 开始游戏", web_app=WebAppInfo(url=web_app_url))],
        [
            InlineKeyboardButton("📢 分享邀请", switch_inline_query=f"join {room['invite_code']}"),
            InlineKeyboardButton("🔄 刷新", callback_data=f"refresh_{room_id}")
        ],
        [InlineKeyboardButton("🚪 离开房间", callback_data=f"leave_{room_id}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')


async def join_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """加入房间"""
    user = update.effective_user
    
    if not context.args:
        await update.message.reply_text("请输入房间号: /join [房间号]")
        return
    
    room_id = context.args[0].upper()
    if room_id not in rooms:
        await update.message.reply_text("❌ 房间不存在")
        return
    
    success = join_room_internal(room_id, user.id, user.username or user.first_name, user.first_name)
    if success:
        await update.message.reply_text(f"✅ 成功加入房间 {room_id}！")
        await show_game_buttons(update, context, room_id)
    else:
        await update.message.reply_text("❌ 加入失败")


async def leave_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """离开房间"""
    user = update.effective_user
    
    if user.id not in player_to_room:
        await update.message.reply_text("你不在任何房间中")
        return
    
    room_id = player_to_room[user.id]
    if room_id in rooms:
        rooms[room_id]['players'] = [p for p in rooms[room_id]['players'] if p['id'] != user.id]
        if len(rooms[room_id]['players']) == 0:
            del rooms[room_id]
    
    del player_to_room[user.id]
    await update.message.reply_text(f"✅ 已离开房间")


async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """显示规则"""
    rules = (
        "📖 德州扑克游戏规则\n\n"
        "🎯 基本玩法:\n"
        "• 每人发2张底牌，5张公共牌\n"
        "• 用最好的5张牌组成牌型\n"
        "• 可弃牌、跟注、加注或全押\n\n"
        "🏆 牌型大小:\n"
        "1. 皇家同花顺\n"
        "2. 同花顺\n"
        "3. 四条\n"
        "4. 葫芦\n"
        "5. 同花\n"
        "6. 顺子\n"
        "7. 三条\n"
        "8. 两对\n"
        "9. 一对\n"
        "10. 高牌"
    )
    await update.message.reply_text(rules)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """帮助"""
    help_text = (
        "📖 命令列表\n\n"
        "/start - 开始使用\n"
        "/newgame - 创建房间\n"
        "/join [房间号] - 加入房间\n"
        "/leave - 离开房间\n"
        "/rules - 游戏规则\n"
        "/help - 帮助"
    )
    await update.message.reply_text(help_text)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """按钮回调"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user = update.effective_user
    
    if data == "create_room":
        await query.delete_message()
        await new_game(update, context)
    elif data == "show_rules":
        await show_rules(update, context)
    elif data.startswith("refresh_"):
        room_id = data.split("_")[1]
        await show_game_buttons(update, context, room_id)
    elif data.startswith("leave_"):
        room_id = data.split("_")[1]
        if user.id in player_to_room:
            del player_to_room[user.id]
        await query.edit_message_text("✅ 已离开房间")


async def cleanup_task():
    """清理过期房间"""
    while True:
        now = time.time()
        expired = [rid for rid, r in rooms.items() if now - r['created_at'] > 3600]
        for rid in expired:
            del rooms[rid]
        await asyncio.sleep(300)


def main():
    if not BOT_TOKEN:
        logger.error("请设置 TELEGRAM_BOT_TOKEN")
        return
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('newgame', new_game))
    application.add_handler(CommandHandler('join', join_room))
    application.add_handler(CommandHandler('leave', leave_room))
    application.add_handler(CommandHandler('rules', show_rules))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    loop = asyncio.get_event_loop()
    loop.create_task(cleanup_task())
    
    logger.info("Bot 启动中...")
    application.run_polling()


if __name__ == '__main__':
    main()
