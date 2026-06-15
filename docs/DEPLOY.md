# 部署指南

> ⚠️ **非常重要：Worker 和 Pages 是两个独立部署！**
> - **Worker** = 后端Bot Webhook = 部署 `workers/` 代码
> - **Pages** = 前端Web App = 部署 `frontend/` 代码
> - 它们是两个完全分开的服务，有各自的域名！不要搞混！

## 🚀 一键部署

[![Deploy to Cloudflare Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/yourusername/telegram-poker-bot)

---

## 📋 手动部署

### 1. 创建 Telegram Bot

1. 打开 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建Bot
3. 保存获得的 **Bot Token**

### 2. 部署 Cloudflare Worker

```bash
cd workers
npm install
npm run deploy
```

### 3. 部署前端到 Cloudflare Pages

```bash
cd frontend
npm install
npm run build
npx wrangler pages deploy dist
```

### 4. 设置 Webhook

```bash
curl "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook" \
  -d '{"url": "https://your-worker.workers.dev/webhook", "secret_token": "your-secret"}'
```

---

## ⚙️ 环境变量

| 变量 | 说明 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | Bot Token |
| `TELEGRAM_WEB_APP_URL` | Pages 域名 |
| `WEBHOOK_SECRET` | Webhook 密钥 |

---

## 🎯 本地开发

```bash
# 启动 Bot
python src/bot.py

# 启动前端
cd frontend && npm run dev

# 启动 Worker
cd workers && npm run dev
```
