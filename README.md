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
│   ├── game/              # 游戏逻辑
│   ├── models/            # 数据模型
│   └── utils/             # 工具函数
├── frontend/              # Telegram Web App (Vue3)
│   ├── src/
│   ├── public/
│   └── package.json
├── workers/               # Cloudflare Workers
│   ├── src/
│   ├── wrangler.toml
│   └── package.json
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
CLOUDFLARE_ACCOUNT_ID=your_account_id
```

### 3. 启动开发服务

```bash
# 启动Bot
python src/bot.py

# 启动前端开发服务器
cd frontend && npm run dev

# 启动Workers本地预览
cd workers && npm run dev
```

## 📖 使用说明

### Bot命令

- `/start` - 开始使用Bot
- `/newgame` - 创建新游戏房间
- `/join [room_id]` - 加入指定房间
- `/rules` - 查看游戏规则
- `/help` - 查看帮助

### 游戏流程

1. 在私聊或群聊中发送 `/newgame` 创建房间
2. Bot会生成邀请链接和Web App按钮
3. 好友点击链接或按钮加入游戏
4. 人数足够后自动开始游戏
5. 通过Web App进行下注、弃牌等操作

## 🎲 游戏规则

### 基本规则
- 使用标准52张扑克牌
- 每位玩家发2张底牌
- 公共牌分三轮发出：翻牌(3张)、转牌(1张)、河牌(1张)
- 玩家可选择：弃牌(Fold)、过牌(Check)、跟注(Call)、加注(Raise)、全押(All-in)

### 牌型大小
1. 皇家同花顺 (Royal Flush)
2. 同花顺 (Straight Flush)
3. 四条 (Four of a Kind)
4. 葫芦 (Full House)
5. 同花 (Flush)
6. 顺子 (Straight)
7. 三条 (Three of a Kind)
8. 两对 (Two Pair)
9. 一对 (One Pair)
10. 高牌 (High Card)

## 🔧 部署指南

详细部署说明请查看 [DEPLOY.md](./docs/DEPLOY.md)

## 📄 许可证

MIT License
