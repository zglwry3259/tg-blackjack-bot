# 📁 项目文件结构说明

## 完整文件列表

```
telegram-poker-bot/
├── 📄 README.md                          # 项目说明文档
├── 📄 PROJECT_STRUCTURE.md               # 本文件
├── 📄 requirements.txt                   # Python依赖
├── 📄 .env.example                       # 环境变量示例
├── 📄 .gitignore                         # Git忽略文件
├── 📄 app.json                           # Cloudflare一键部署配置
│
├── 📂 src/                               # Python Bot 后端
│   ├── 📄 bot.py                         # Bot主入口
│   └── 📂 game/
│       ├── 📄 __init__.py
│       ├── 📄 engine.py                  # 德州扑克游戏引擎核心
│       └── 📄 room_manager.py            # 房间管理器
│
├── 📂 frontend/                          # Telegram Web App 前端
│   ├── 📄 package.json
│   ├── 📄 vite.config.js
│   ├── 📄 tailwind.config.js
│   ├── 📄 postcss.config.js
│   ├── 📄 index.html
│   └── 📂 src/
│       ├── 📄 main.js
│       ├── 📄 style.css
│       ├── 📄 App.vue
│       ├── 📂 components/
│       │   ├── 📄 Lobby.vue              # 大厅组件
│       │   ├── 📄 GameTable.vue          # 游戏桌组件
│       │   ├── 📄 PlayingCard.vue        # 扑克牌组件
│       │   ├── 📄 PlayerSeat.vue         # 玩家座位组件
│       │   └── 📄 ActionButtons.vue      # 操作按钮组件
│       └── 📂 composables/
│           └── 📄 useGameState.js        # 游戏状态管理
│
├── 📂 workers/                           # Cloudflare Workers
│   ├── 📄 package.json
│   ├── 📄 wrangler.toml                  # Wrangler配置
│   ├── 📄 schema.sql                     # D1数据库Schema
│   └── 📂 src/
│       └── 📄 index.js                   # Worker主入口
│
├── 📂 docs/                              # 文档
│   └── 📄 DEPLOY.md                      # 部署指南
│
├── 📂 scripts/                           # 脚本
│   └── 📄 deploy.sh                      # 部署脚本
│
└── 📂 .github/
    └── 📂 workflows/
        └── 📄 deploy.yml                 # GitHub Actions自动部署
```

## 🎯 核心功能模块

### 1. 游戏引擎 (src/game/engine.py)
- ✅ 完整的德州扑克游戏规则实现
- ✅ 牌型评估器（支持所有牌型判断）
- ✅ 玩家管理（筹码、下注、弃牌、全押）
- ✅ 游戏阶段管理（翻牌前、翻牌、转牌、河牌、摊牌）
- ✅ 自动发牌和胜负判定

### 2. 房间系统 (src/game/room_manager.py)
- ✅ 房间创建和加入
- ✅ 邀请码生成
- ✅ 公开/私人房间
- ✅ 玩家房间映射
- ✅ 自动清理不活跃房间

### 3. Telegram Bot (src/bot.py)
- ✅ 命令处理（/start, /newgame, /join, /leave等）
- ✅ 内联键盘按钮
- ✅ Web App按钮集成
- ✅ 邀请链接生成
- ✅ 群聊支持

### 4. Web App 前端 (frontend/)
- ✅ Vue 3 + Vite + Tailwind CSS
- ✅ 响应式移动端设计
- ✅ 游戏桌界面
- ✅ 扑克牌动画效果
- ✅ 玩家座位显示
- ✅ 下注操作界面

### 5. Cloudflare Worker (workers/)
- ✅ Telegram Webhook处理
- ✅ KV存储房间状态
- ✅ D1数据库持久化
- ✅ 游戏API接口
- ✅ 安全验证

## 🚀 快速开始

### 本地运行Bot
```bash
cd telegram-poker-bot
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入你的Bot Token
python src/bot.py
```

### 部署到Cloudflare
详细步骤见 [docs/DEPLOY.md](./docs/DEPLOY.md)

## 🔗 Telegram Bot 命令列表

| 命令 | 功能 |
|------|------|
| `/start` | 开始使用Bot |
| `/newgame` | 创建新游戏房间 |
| `/join [房间号]` | 加入指定房间 |
| `/rooms` | 查看公开房间列表 |
| `/leave` | 离开当前房间 |
| `/rules` | 查看游戏规则 |
| `/help` | 显示帮助 |

## 💡 技术栈

- **后端**: Python 3 + python-telegram-bot v20
- **前端**: Vue 3 + Vite + Tailwind CSS
- **云服务**: Cloudflare Workers + Pages + D1 + KV
- **部署**: GitHub Actions + Wrangler CLI
