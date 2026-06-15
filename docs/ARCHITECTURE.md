# 🏗️ 部署架构详细说明

## 一、整体架构设计

### 1.1 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    Telegram 生态系统                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐      ┌──────────────────────────────┐    │
│  │   Bot 消息    │      │    Telegram Web App (Mini App)│    │
│  └──────┬───────┘      └──────────────┬───────────────┘    │
└─────────┼───────────────────────────────┼───────────────────┘
          │                               │
          ▼                               ▼
┌──────────────────┐          ┌──────────────────────────┐
│ Cloudflare Worker│          │   Cloudflare Pages       │
│  (Webhook + API) │          │   (静态前端)             │
├──────────────────┤          ├──────────────────────────┤
│ • /webhook       │          │ • Vue 3 构建产物         │
│ • /api/*         │          │ • HTML/CSS/JS           │
│ • KV存储房间状态 │          │ • 纯静态，无服务端逻辑    │
└────────┬─────────┘          └──────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Cloudflare KV    │
│ (房间数据)       │
└──────────────────┘
```

---

## 二、架构详细说明

### 2.1 后端：Cloudflare Worker

**✅ 部署位置：Cloudflare Worker**

**功能职责：**
1. **Telegram Webhook 接收** - `/webhook` 端点接收Telegram服务器推送的消息
2. **Bot命令处理** - 处理 `/start`, `/newgame`, `/join` 等所有Bot命令
3. **内联按钮回调** - 处理Web App和键盘按钮的回调
4. **游戏状态API** - `/api/rooms/*` 提供游戏状态查询和更新接口
5. **房间数据存储** - 通过KV存储持久化房间信息

**为什么选择Worker而不是Pages Functions？**
- Worker支持更灵活的路由配置
- Worker有独立的域名，便于设置Webhook
- Worker可以直接绑定KV/D1，无需额外配置
- Pages Functions主要用于API路由，不适合长连接Webhook

---

### 2.2 前端：Cloudflare Pages

**✅ 部署位置：Cloudflare Pages**

**功能职责：**
1. **Telegram Web App 界面** - Vue 3单页应用
2. **游戏桌渲染** - 扑克牌、玩家座位、底池显示
3. **用户交互** - 下注、弃牌、加注等操作按钮
4. **API通信** - 通过HTTP调用Worker的API接口

**为什么选择Pages？**
- Pages专为静态站点优化，CDN全球加速
- 自动HTTPS，符合Telegram Web App要求
- 支持GitHub自动部署，构建流程简单
- 免费额度充足，适合前端静态资源

---

### 2.3 分离部署架构

**✅ 两部分完全分开部署**

| 组件 | 部署位置 | 访问域名 | 职责 |
|------|---------|---------|------|
| **后端** | Cloudflare Worker | `poker-bot.xxx.workers.dev` | Webhook + API |
| **前端** | Cloudflare Pages | `poker-app.pages.dev` | Web App界面 |

**通信方式：**
- 前端通过 `fetch()` 调用后端Worker的API
- 后端通过Telegram Bot API发送消息给用户
- 两者通过CORS配置实现跨域通信

---

## 三、Worker 部署详细步骤

### 3.1 前置准备

```bash
# 1. 安装 wrangler CLI
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login
```

### 3.2 创建 KV 命名空间

```bash
# 创建房间存储KV
wrangler kv:namespace create ROOMS

# 输出示例：
# { binding = "ROOMS", id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", preview_id = "..." }
```

### 3.3 配置 wrangler.toml

```toml
name = "telegram-poker-bot"           # Worker名称（全局唯一）
main = "index.js"                      # 入口文件
compatibility_date = "2024-01-01"     # 运行时版本

# KV 命名空间绑定
[[kv_namespaces]]
binding = "ROOMS"                      # 代码中访问的变量名
id = "你的KV命名空间ID"                 # 上一步获得的ID

# 环境变量（运行时注入）
[vars]
TELEGRAM_BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
TELEGRAM_WEB_APP_URL = "https://your-app.pages.dev"
WEBHOOK_SECRET = "随机生成的安全密钥"
```

### 3.4 本地开发测试

```bash
cd workers
npm install

# 启动本地开发服务器（端口8787）
npm run dev

# 测试健康检查
curl http://localhost:8787/health
```

### 3.5 部署到生产环境

```bash
# 部署Worker
npm run deploy

# 部署成功后获得域名：
# https://telegram-poker-bot.your-username.workers.dev
```

### 3.6 设置 Telegram Webhook

```bash
# 设置Webhook地址
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://telegram-poker-bot.your-username.workers.dev/webhook",
    "secret_token": "你的WEBHOOK_SECRET"
  }'

# 验证Webhook设置
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

---

## 四、Pages 部署详细步骤

### 4.1 本地构建测试

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（端口3000）
npm run dev

# 生产构建
npm run build
# 构建产物输出到 dist/ 目录
```

### 4.2 Pages 配置

**方式一：通过 Wrangler CLI 部署**
```bash
# 首次部署（创建Pages项目）
npx wrangler pages deploy dist \
  --project-name=telegram-poker \
  --production

# 后续部署
npx wrangler pages deploy dist
```

**方式二：通过 GitHub 自动部署**

1. 在 Cloudflare Dashboard 进入 **Workers & Pages**
2. 点击 **Create application** → **Pages** → **Connect to Git**
3. 选择你的GitHub仓库
4. 配置构建设置：
   - **Project name**: `telegram-poker`
   - **Production branch**: `main`
   - **Framework preset**: `Vite`
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Build output directory**: `frontend/dist`

### 4.3 Pages 环境变量

在 Cloudflare Dashboard → Pages → 你的项目 → Settings → Environment variables：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `VITE_API_BASE_URL` | Worker API地址 | `https://poker-bot.xxx.workers.dev` |

> ⚠️ **注意**：Pages的环境变量是**构建时**注入的，修改后需要重新触发构建

---

## 五、推荐部署流程（先后顺序）

### 📋 正确的部署顺序（非常重要！）

```
第1步：创建 Cloudflare 资源
  ├─ 创建 KV 命名空间
  └─ （可选）创建 D1 数据库

第2步：部署 Worker 后端
  ├─ 配置 wrangler.toml (填入KV ID)
  ├─ 配置环境变量 (Bot Token等)
  ├─ 部署Worker
  └─ ✅ 获得 Worker 域名

第3步：部署 Pages 前端
  ├─ 配置 VITE_API_BASE_URL = Worker域名
  ├─ 构建前端
  ├─ 部署到Pages
  └─ ✅ 获得 Pages 域名

第4步：更新配置
  ├─ 更新Worker中的 TELEGRAM_WEB_APP_URL = Pages域名
  ├─ 重新部署Worker
  └─ 设置Telegram Webhook

第5步：配置 BotFather
  └─ 设置 /newapp 域名 = Pages域名
```

### ⚠️ 关键注意事项

1. **必须先部署Worker**：前端需要Worker的API地址
2. **必须再部署前端**：获得Pages域名后需要更新Worker配置
3. **必须重新部署Worker**：更新TELEGRAM_WEB_APP_URL后要重新部署
4. **最后设置Webhook**：确保Worker部署完成后再设置

---

## 六、一键部署按钮详解

### 6.1 app.json 配置原理

Cloudflare的一键部署按钮通过 `app.json` 配置部署流程：

```json
{
  "name": "Telegram Poker Bot",
  "description": "完整的Telegram德州扑克游戏Bot",
  
  // 声明需要的Cloudflare资源
  "cloudflare": {
    "workers": true,      // 需要部署Worker
    "pages": true,        // 需要部署Pages
    "d1": true,           // 需要D1数据库
    "kv": true            // 需要KV命名空间
  },
  
  // 用户需要填写的环境变量
  "env": {
    "TELEGRAM_BOT_TOKEN": {
      "description": "从 @BotFather 获取的Bot Token",
      "required": true
    },
    "TELEGRAM_WEB_APP_URL": {
      "description": "部署后获得的Pages域名",
      "required": true
    },
    "WEBHOOK_SECRET": {
      "description": "Webhook验证密钥",
      "generator": "secret",    // 自动生成随机密钥
      "required": true
    }
  }
}
```

### 6.2 一键部署自动流程

当用户点击 **Deploy to Cloudflare** 按钮时：

```
用户点击按钮
    ↓
1. 跳转至 Cloudflare 授权页面
    ↓
2. 用户授权 GitHub + Cloudflare
    ↓
3. 自动 Fork 仓库到用户 GitHub
    ↓
4. 自动创建 Cloudflare 资源：
   ├─ ✅ 创建 KV 命名空间 ROOMS
   ├─ ✅ 创建 D1 数据库（如配置）
   └─ ✅ 绑定到 Worker
    ↓
5. 自动配置环境变量
   ├─ 用户填写 TELEGRAM_BOT_TOKEN
   ├─ 自动生成 WEBHOOK_SECRET
   └─ 注入到 Worker Secrets
    ↓
6. 触发 GitHub Actions 自动部署
   ├─ 部署 Worker
   └─ 部署 Pages
    ↓
✅ 部署完成！
```

### 6.3 一键部署的局限性

**❌ 目前一键部署按钮的限制：**

1. **不能同时部署Worker + Pages**
   - 官方一键部署按钮**只支持Worker**
   - Pages需要单独配置GitHub Actions部署

2. **D1/KV自动创建**
   - KV可以通过wrangler.toml自动创建
   - D1需要手动创建后绑定ID

3. **BotFather配置无法自动化**
   - 需要用户手动在 @BotFather 设置Web App域名

---

## 七、实际推荐的部署方案

### 7.1 生产环境推荐配置

```
┌─────────────────────────────────────────────────┐
│              推荐部署架构                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  🔷 Worker (单独部署)                            │
│     ├─ 绑定 KV: ROOMS (房间状态)                │
│     ├─ 绑定 D1: poker_db (用户数据/历史)         │
│     └─ 环境变量: Secrets 加密存储                │
│                                                 │
│  🔷 Pages (单独部署)                             │
│     ├─ GitHub Actions 自动构建部署               │
│     └─ 环境变量: 构建时注入                      │
│                                                 │
│  🔷 自定义域名（可选）                            │
│     ├─ api.example.com → Worker                 │
│     └─ app.example.com → Pages                  │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 7.2 环境变量配置最佳实践

| 位置 | 变量 | 配置方式 | 安全性 |
|------|------|---------|--------|
| **Worker** | `TELEGRAM_BOT_TOKEN` | Wrangler Secrets | ✅ 加密 |
| **Worker** | `WEBHOOK_SECRET` | Wrangler Secrets | ✅ 加密 |
| **Worker** | `TELEGRAM_WEB_APP_URL` | wrangler.toml [vars] | ⚠️ 明文 |
| **Pages** | `VITE_API_URL` | Pages环境变量 | ⚠️ 前端可见 |

> 🔐 **安全提示**：敏感信息（如Bot Token）必须使用Secrets，不要写在wrangler.toml中

---

## 八、故障排查指南

### 8.1 Worker 常见问题

**❌ Webhook 不响应**
- 检查 `wrangler tail` 查看日志
- 验证Webhook URL是否可公网访问
- 检查 `WEBHOOK_SECRET` 是否匹配

**❌ KV 操作失败**
- 确认 wrangler.toml 中 KV ID 正确
- 确认 binding 名称与代码一致
- 本地开发需要配置 `preview_id`

### 8.2 Pages 常见问题

**❌ 前端无法调用API**
- 检查Worker是否配置了CORS
- 确认 `VITE_API_BASE_URL` 正确
- 检查浏览器控制台跨域错误

**❌ 构建失败**
- 确认构建命令路径正确
- 检查Node.js版本（推荐18+）
- 查看构建日志

### 8.3 Telegram Bot 常见问题

**❌ Web App 打不开**
- 确认使用 HTTPS（Telegram强制要求）
- 在 @BotFather 执行 `/newapp` 设置正确域名
- 清除Telegram缓存重试

---

## 📝 总结

| 组件 | 部署位置 | 优点 | 注意事项 |
|------|---------|------|---------|
| **后端API/Webhook** | Cloudflare Worker | 低延迟、Serverless、KV绑定 | 先部署 |
| **前端Web App** | Cloudflare Pages | CDN加速、静态优化 | 后部署，需要Worker地址 |
| **数据存储** | Cloudflare KV | 键值存储、全球分布 | 适合房间状态 |
| **持久化** | Cloudflare D1 | SQL数据库、事务 | 用户数据/游戏历史 |

**部署顺序口诀：先后端，再前端，最后配置BotFather**
