# 🚀 从零开始：超详细部署教程（新手友好）

> ⚠️ **非常重要：Worker 和 Pages 是两个独立部署！**
> - **Worker** = 后端Bot Webhook = 部署 `workers/` 代码
> - **Pages** = 前端Web App = 部署 `frontend/` 代码
> - 它们是两个完全分开的服务，有各自的域名！不要搞混！

> ✅ **写给新手**：本教程每一步都有具体命令，照着复制粘贴即可完成！
>
> ⏱️ **预计用时**：30-45分钟
>
> 🎯 **最终目标**：拥有一个可以在Telegram玩德州扑克的Bot

---

## 📋 第0章：前置准备清单（必须先完成！）

在开始之前，请确保你准备好了以下4样东西：

| # | 需要准备 | 用途 |
|---|---------|------|
| 1 | 📧 Cloudflare账号 | 部署后端和前端 |
| 2 | 🤖 Telegram Bot Token | Bot的身份证 |
| 3 | 🐙 GitHub账号 | 存放代码，自动部署 |
| 4 | 💻 电脑（安装Node.js） | 运行命令 |

---

## 🔧 0.1 安装必要工具

### ⚠️ Python 版本兼容性说明（重要！）

**重要提示：** 推荐使用 Python 3.11 或 3.12。Python 3.13 存在 pydantic-core 兼容性问题。

检查Python版本：
```bash
python --version  # 应该是 3.11.x 或 3.12.x
```

如果是Python 3.13，请降级或使用：
```bash
# 使用pyenv切换版本（推荐）
pyenv install 3.12.0
pyenv global 3.12.0
```

### 0.1.1 安装 Node.js

【新手提示】Node.js是运行JavaScript的环境，必须安装！

1. 打开官网：https://nodejs.org/
2. 下载 **LTS版本**（推荐18.x或20.x）
3. 双击安装，一路点"下一步"

**验证安装成功**（打开命令提示符/终端）：
```bash
node --version
# 应该显示类似 v20.10.0

npm --version
# 应该显示类似 10.2.3
```

### 0.1.2 安装 Git

1. 打开官网：https://git-scm.com/downloads
2. 下载对应系统版本
3. 安装，一路默认选项

**验证安装成功**：
```bash
git --version
# 显示类似 git version 2.43.0
```

---

## 🤖 0.2 创建 Telegram Bot（最关键！）

【重要】这一步必须做对，否则整个Bot无法工作！

### 步骤1：打开 @BotFather

1. 打开Telegram
2. 搜索 `@BotFather`（有蓝色对勾的官方账号）
3. 点击开始

### 步骤2：创建新Bot

发送命令：
```
/newbot
```

BotFather会回复：
```
Alright, a new bot. How are we going to call it? Please choose a name for your bot.
```

### 步骤3：设置Bot名称

输入你想要的Bot显示名称（可以中文）：
```
德州扑克游戏Bot
```

### 步骤4：设置Bot用户名

【注意】用户名**必须以 bot 结尾**，且全局唯一！
```
MyTexasPokerBot
```

✅ 如果成功，你会收到这样的消息：
```
Done! Congratulations on your new bot. You will find it at t.me/MyTexasPokerBot.

Use this token to access the HTTP API:
1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ1234567890

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

### ✅ 保存你的 Bot Token！

把这串字符复制保存好，后面要用：
```
1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ1234567890
```

---

## ☁️ 0.3 注册 Cloudflare 账号

1. 打开 https://dash.cloudflare.com/sign-up
2. 输入邮箱、设置密码
3. 验证邮箱
4. 登录成功后，你会看到Cloudflare控制台

---

## 🐙 0.4 注册 GitHub 账号

1. 打开 https://github.com/signup
2. 输入邮箱、用户名、密码
3. 验证邮箱
4. 完成注册

---

## 🚀 0.5 关于"一键部署"的诚实说明

> 💡 **新手必读**：点击按钮前请先了解真实情况！

### ✅ "Deploy to Cloudflare" 按钮能自动完成：

- ✅ 自动创建Cloudflare Worker项目
- ✅ 自动创建KV命名空间并绑定
- ✅ 自动创建D1数据库（如果配置）
- ✅ 自动部署Worker代码
- ✅ 自动设置大部分环境变量
- ✅ GitHub仓库自动连接

### ❌ 一键部署**不能**自动完成（必须手动）：

1. **@BotFather 创建Bot和获取Token**（Telegram限制，无法自动化）
2. **设置Telegram Webhook URL**（需要Worker部署后的域名）
3. **@BotFather 设置Web App域名**（需要Pages部署后的域名）
4. **部署Cloudflare Pages前端**（官方按钮只支持Worker）
5. **更新 TELEGRAM_WEB_APP_URL 环境变量**

### 一键部署完整流程（用户点击按钮后）：

```
1. 用户点击"Deploy to Cloudflare"按钮
   ↓
2. 跳转到Cloudflare，授权GitHub权限
   ↓
3. Cloudflare自动fork仓库到用户GitHub
   ↓
4. 用户填写 TELEGRAM_BOT_TOKEN（唯一必填项）
   ↓
5. 点击"Deploy"，等待3-5分钟
   ↓
6. ✅ Worker部署完成，获得 xxx.workers.dev 域名
   ↓
7. ⚠️ 用户手动执行剩余3步：
   ├─ 部署Pages前端（5分钟）
   ├─ 设置Webhook（1分钟）
   └─ @BotFather配置Web App域名（1分钟）
```

### 🎯 推荐部署路径

| 用户类型 | 推荐方式 | 总用时 |
|---------|---------|--------|
| **纯新手** | 一键部署Worker + 手动完成剩余3步 | 10分钟 |
| **开发者** | 全程命令行部署 | 15分钟 |

---

## 📦 第1章：准备代码并上传到GitHub

### 1.1 下载项目源码

1. 下载我给你的 `telegram-poker-bot.zip`
2. 解压到一个文件夹，比如 `D:\telegram-poker-bot`

### 1.2 创建GitHub仓库

1. 打开 https://github.com/new
2. 填写：
   - **Repository name**: `telegram-poker-bot`
   - **Public**（选公开）
   - ✅ 不要勾选 "Add a README file"
3. 点击 **Create repository**

### 1.3 上传代码到GitHub

【新手提示】打开"命令提示符"（Windows）或"终端"（Mac），一行一行执行！

```bash
# 第1步：进入解压后的文件夹（改成你自己的路径！）
cd D:\telegram-poker-bot

# 第2步：初始化git
git init

# 第3步：添加所有文件
git add .

# 第4步：提交
git commit -m "Initial commit"

# 第5步：连接到你的GitHub仓库（改成你自己的地址！）
git remote add origin https://github.com/你的用户名/telegram-poker-bot.git

# 第6步：上传
git push -u origin main
```

✅ 刷新GitHub页面，你应该能看到所有代码了！

---

## ⚡ 第2章：部署 Cloudflare Worker（后端）

### 2.1 安装 wrangler 命令行工具

```bash
npm install -g wrangler
```

验证安装：
```bash
wrangler --version
# 显示类似 3.22.4
```

### 2.2 登录 Cloudflare

```bash
wrangler login
```

1. 浏览器会自动打开Cloudflare授权页面
2. 点击 **Allow** 允许访问
3. 回到命令行，看到 "Successfully logged in." 就成功了！

### 2.3 创建 KV 命名空间（存储房间数据）

【重要】KV是Cloudflare的数据库，用来存储游戏房间信息

```bash
wrangler kv:namespace create ROOMS
```

✅ 你会看到输出：
```
{ binding = "ROOMS", id = "abc123def456ghi789jkl012mno345pqr", preview_id = "..." }
```

### ✅ 保存你的 KV ID！

把这串ID复制保存好：
```
abc123def456ghi789jkl012mno345pqr
```

### 2.4 配置 Worker 设置

用记事本打开 `workers/wrangler.toml` 文件，修改以下内容：

```toml
# ==========================================
# 【必须修改】下面这3个配置
# ==========================================

# 1. Worker名称（英文，全局唯一）
name = "my-texas-poker-bot"          

# 2. 【重要】粘贴你刚才创建的KV ID
[[kv_namespaces]]
binding = "ROOMS"
id = "abc123def456ghi789jkl012mno345pqr"   # ← 这里改成你的KV ID

# 3. 环境变量配置
[vars]
# 粘贴你从BotFather获得的Token
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ1234567890"

# 【先留空】等下部署完Pages后再回来填！
TELEGRAM_WEB_APP_URL = ""

# 【随便写一串随机字符】比如你的生日+随机字母
WEBHOOK_SECRET = "mySuperSecretKey123456"
```

【新手提示】
- `TELEGRAM_BOT_TOKEN`：从 @BotFather 获取
- `TELEGRAM_WEB_APP_URL`：**先空着**，部署完Pages再填
- `WEBHOOK_SECRET`：随便写，比如 `MyPokerBot2024!`

### 2.5 部署 Worker！

```bash
# 进入workers目录
cd workers

# 安装依赖（只需要运行一次）
npm install

# 部署！
npm run deploy
```

✅ 成功后你会看到：
```
Deployed your Worker to:
https://my-texas-poker-bot.yourname.workers.dev
```

### ✅ 保存你的 Worker 域名！

```
https://my-texas-poker-bot.yourname.workers.dev
```

### 2.6 验证Worker是否工作

在浏览器打开你的Worker域名，应该看到：
```
Telegram Poker Bot Worker
```

---

## 🎨 第3章：部署 Cloudflare Pages（前端）

### 方式A：通过Dashboard连接GitHub（推荐！自动部署）

#### 3.1 连接GitHub

1. 打开 Cloudflare Dashboard: https://dash.cloudflare.com/
2. 点击左侧 **Workers & Pages**
3. 点击 **Create application**
4. 选择 **Pages** 标签
5. 点击 **Connect to Git**

#### 3.2 选择仓库

1. 选择你刚才创建的 `telegram-poker-bot` 仓库
2. 点击 **Begin setup**

#### 3.3 配置构建设置（非常重要！）

| 配置项 | 填什么 |
|--------|--------|
| **Project name** | `my-texas-poker`（随便写） |
| **Production branch** | `main` |
| **Framework preset** | `None`（不要选Vite！） |
| **Build command** | `cd frontend && npm install && npm run build` |
| **Build output directory** | `frontend/dist` |

#### 3.3.1 环境变量配置（必须）

在 **Environment variables (advanced)** 部分添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `PYTHON_VERSION` | `3.12` | 避免Python 3.13兼容性问题 |
| `NODE_VERSION` | `20` | 指定Node.js版本 |

#### 3.4 点击 **Save and Deploy**

等待1-2分钟，部署完成！

✅ 成功后你会获得Pages域名：
```
https://my-texas-poker.pages.dev
```

### ✅ 保存你的 Pages 域名！

---

### 方式B：命令行部署（备选）

如果你不想用GitHub自动部署，可以手动构建上传：

```bash
# 进入frontend目录
cd frontend

# 安装依赖
npm install

# 构建
npm run build

# 部署到Pages
npx wrangler pages deploy dist --project-name=my-texas-poker
```

---

## 🔄 第4章：关键配置更新（非常重要！不能跳过！）

【重要】现在你有了Pages域名，需要回到Worker更新配置！

### 4.1 更新 Worker 配置

再次打开 `workers/wrangler.toml`，更新：

```toml
[vars]
TELEGRAM_BOT_TOKEN = "你的Bot Token"

# ==========================================
# 【重要】现在填上你的Pages域名！
# ==========================================
TELEGRAM_WEB_APP_URL = "https://my-texas-poker.pages.dev"

WEBHOOK_SECRET = "你的密钥"
```

### 4.2 重新部署 Worker

```bash
# 确保在workers目录
cd workers

# 重新部署！
npm run deploy
```

✅ 这一步**必须做**，否则Bot里的游戏链接会打不开！

---

## 🔗 第5章：设置 Telegram Webhook

【重要】告诉Telegram把消息发到你的Worker

### 5.1 执行Webhook设置命令

打开记事本，把下面命令中的 `<>` 部分替换成你自己的：

```bash
curl "https://api.telegram.org/bot<你的BotToken>/setWebhook" ^
  -H "Content-Type: application/json" ^
  -d "{\"url\": \"<你的Worker域名>/webhook\", \"secret_token\": \"你的WEBHOOK_SECRET\"}"
```

### 完整示例：

```bash
curl "https://api.telegram.org/bot1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ1234567890/setWebhook" ^
  -H "Content-Type: application/json" ^
  -d "{\"url\": \"https://my-texas-poker-bot.yourname.workers.dev/webhook\", \"secret_token\": \"mySuperSecretKey123456\"}"
```

【Windows提示】在命令提示符中执行，注意引号格式

### 5.2 验证Webhook设置成功

```bash
curl "https://api.telegram.org/bot<你的BotToken>/getWebhookInfo"
```

✅ 成功的返回应该包含：
```json
{
  "ok": true,
  "result": {
    "url": "https://my-texas-poker-bot.yourname.workers.dev/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

---

## 🎮 第6章：配置 @BotFather Web App

【重要】让Telegram知道你的Web App域名

### 6.1 设置 Web App 域名

回到 @BotFather，发送：
```
/setdomain
```

BotFather会问选择哪个Bot，选择你刚创建的Bot，然后输入你的Pages域名：
```
https://my-texas-poker.pages.dev
```

### 6.2 设置菜单按钮（可选，推荐）

发送命令给 @BotFather：
```
/setmenubutton
```

选择你的Bot，然后设置：
- 按钮文字：`🎮 开始游戏`
- 打开的网址：`https://my-texas-poker.pages.dev`

---

## ✅ 第7章：完整测试！

恭喜！现在可以测试你的Bot了！

### 7.1 找到你的Bot

在Telegram搜索你的Bot用户名，比如 `@MyTexasPokerBot`

### 7.2 发送命令测试

1. 发送 `/start`
   - ✅ 应该收到欢迎消息

2. 发送 `/newgame`
   - ✅ 应该显示"创建房间成功"
   - ✅ 应该有"🎴 开始游戏"按钮

3. 点击"开始游戏"按钮
   - ✅ 应该打开Web App游戏界面
   - ✅ 能看到游戏桌、扑克牌

4. 发送 `/rules`
   - ✅ 应该显示游戏规则

### 7.3 联机测试

1. 邀请朋友也加入你的Bot
2. 分享邀请链接
3. 测试多人同时在线

---

## ❓ 第8章：常见问题排查 FAQ

### Q1: Bot不回复消息怎么办？

**排查步骤：**
1. 检查Webhook是否设置正确：`getWebhookInfo`
2. 查看Worker日志：`wrangler tail`
3. 确认Bot Token正确
4. 确认Worker域名可访问

### Q2: KV绑定错误？

**错误信息：** `Binding "ROOMS" doesn't exist`

**解决方法：**
1. 确认 `wrangler kv:namespace list` 能看到你的KV
2. 确认 `wrangler.toml` 中的KV ID正确
3. 重新部署：`npm run deploy`

### Q3: Web App 打不开？

**可能原因：**
1. ❌ 不是HTTPS（Telegram强制要求HTTPS）
2. ❌ `TELEGRAM_WEB_APP_URL` 配置错误
3. ❌ @BotFather 的 `/setdomain` 没设置

**解决方法：**
1. 确认用的是Cloudflare Pages域名（自动HTTPS）
2. 确认Worker中 `TELEGRAM_WEB_APP_URL` 与Pages域名一致
3. 重新执行 `/setdomain`

### Q4: 前端无法调用API（CORS错误）？

**解决方法：**
1. Worker中添加CORS头
2. 确认 `VITE_API_BASE_URL` 配置正确
3. 不要用localhost测试Telegram Web App

### Q5: 游戏状态不同步？

**解决方法：**
1. 检查KV绑定是否正确
2. 确认API请求成功
3. 查看浏览器控制台Network标签

### Q6: Pages构建报错 `no such file or directory, open '/.../package.json'`

**错误信息：**
```
npm error Could not read package.json: Error: ENOENT: no such file or directory
```

**原因：** Pages默认在根目录构建，但前端代码在 `frontend/` 子目录

**解决方案：**
1. ✅ 根目录已有 package.json（本项目已修复）
2. ✅ 构建命令填：`npm run build` 或 `cd frontend && npm install && npm run build`
3. ✅ 输出目录填：`frontend/dist`

### Q7: Tailwind构建报错 `The 'text-poker-xxx' class does not exist`

**错误信息：**
```
The `text-poker-black` class does not exist. If `text-poker-black` is a custom class, make sure it is defined within a `@layer` directive.
```

**原因：** tailwind.config.js中没有定义poker自定义颜色

**解决方案：**
1. ✅ 项目已修复，tailwind.config.js已添加完整poker颜色定义
2. ✅ 清除缓存重新构建：删除 `frontend/node_modules` 和 `frontend/package-lock.json` 重新安装
3. ✅ 或使用标准Tailwind类：`text-gray-800` 代替 `text-poker-black`

### Q8: 安装依赖时报错 `pydantic-core` 构建失败？

**错误信息：**
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
ERROR: Failed building wheel for pydantic-core
```

**原因：** Python 3.13 与旧版 pydantic-core 不兼容

**解决方案（三选一）：**
1. ✅ **降级 Python 到 3.11 或 3.12**（推荐）
2. ✅ 更新 requirements.txt 使用 `pydantic>=2.9.0` 和 `pydantic-core>=2.23.0`
3. ✅ Cloudflare Pages 设置环境变量 `PYTHON_VERSION=3.12`

---

## 🎉 部署完成！

你现在拥有了：
- ✅ 一个运行在Cloudflare Worker上的Telegram Bot后端
- ✅ 一个运行在Cloudflare Pages上的Web App前端
- ✅ 支持多人联机的德州扑克游戏

---

## 📝 部署成功检查清单

- [ ] Cloudflare账号注册完成
- [ ] Telegram Bot创建完成，Token已保存
- [ ] GitHub仓库创建，代码已上传
- [ ] KV命名空间创建完成
- [ ] Worker部署成功，获得Worker域名
- [ ] Pages部署成功，获得Pages域名
- [ ] Worker配置已更新TELEGRAM_WEB_APP_URL
- [ ] Worker已重新部署
- [ ] Telegram Webhook已设置
- [ ] @BotFather /setdomain 已配置
- [ ] Bot发送 /start 有回复
- [ ] /newgame 能创建房间
- [ ] Web App 能正常打开

---

## 💡 给新手的最后建议

1. **不要跳步**：按顺序一步一步来
2. **复制粘贴**：命令尽量复制，不要手动输入
3. **保存好各种ID和Token**：建个记事本存起来
4. **遇到错误先看日志**：`wrangler tail` 是最好的调试工具
5. **耐心等待**：Cloudflare部署有时需要1-2分钟生效

祝你部署顺利！🎰
