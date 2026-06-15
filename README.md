# 🎰 Telegram 德州扑克 Bot

一个完整的Telegram德州扑克游戏Bot，支持多人联机对战，通过Telegram Web App进行游戏，可一键邀请好友或在群内发起游戏。

## ✨ 特性

- 🎮 **完整德州扑克游戏逻辑** - 支持2-10人联机对战
- 📱 **Telegram Web App** - 精美的移动端游戏界面
- 🔗 **房间系统** - 创建私人/公开房间，生成邀请链接
- 👥 **群支持** - 直接在Telegram群内发起游戏
- ☁️ **Cloudflare部署** - Serverless架构，全球加速
- 🚀 **一键部署** - GitHub Actions + Cloudflare自动部署

## 🚀 一键部署

[![Deploy to Cloudflare Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/yourusername/telegram-poker-bot)

## 📋 前置要求

- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- Cloudflare 账号
- GitHub 账号

## 🏗️ 项目结构

```
telegram-poker-bot/
├── src/                    # Python Bot 后端
│   ├── bot.py             # Bot主入口
│   └── game/              # 游戏逻辑
├── frontend/              # Telegram Web App (Vue3)
├── workers/               # Cloudflare Workers
├── docs/                  # 文档
└── README.md
```

## 🛠️ 本地开发

### 1. 安装依赖

```bash
# Python后端
pip install -r requirements.txt

# Web App前端
cd frontend && npm install

# Cloudflare Workers
cd workers && npm install
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_WEB_APP_URL=your_web_app_url
```

### 3. 启动开发服务

```bash
# 启动Bot
python src/bot.py
```

## 📖 Bot命令

- `/start` - 开始使用Bot
- `/newgame` - 创建新游戏房间
- `/join [room_id]` - 加入指定房间
- `/rules` - 查看游戏规则
- `/help` - 查看帮助

## 🎲 游戏规则

### 牌型大小（从大到小）
1. 皇家同花顺
2. 同花顺
3. 四条
4. 葫芦
5. 同花
6. 顺子
7. 三条
8. 两对
9. 一对
10. 高牌

## 🔧 部署指南

详细部署说明请查看 [docs/DEPLOY.md](./docs/DEPLOY.md)

## 📄 许可证

MIT License
