# 🚀 真正零命令行部署指南（全程网页点击）

> ⚠️ **非常重要：Worker 和 Pages 是两个独立部署！**
> - **Worker** = 后端Bot Webhook = 部署 `workers/` 代码
> - **Pages** = 前端Web App = 部署 `frontend/` 代码
> - 它们是两个完全分开的服务，有各自的域名！不要搞混！

> ✅ **推荐给所有用户**：不需要命令行，不需要git，不需要编程基础
>
> ⏱️ **预计用时**：15分钟
>
> 🎯 **你需要做的**：复制粘贴 + 点击按钮 + 填写几个文本框

---

## 📋 准备工作（5分钟）

### 第1步：创建 Telegram Bot

1. 打开 Telegram，搜索 **@BotFather**（有蓝色对勾的官方账号）
2. 点击 **开始**
3. 发送命令：
   ```
   /newbot
   ```
4. 按提示输入Bot名称（可以中文）
5. 输入Bot用户名（**必须以bot结尾**，比如：`MyPokerGameBot`）
6. ✅ 成功后你会收到一串 **Bot Token**，复制保存好！

**Token格式示例：**
```
1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ1234567890
```

### 第2步：注册 Cloudflare 账号（免费）

1. 打开 https://dash.cloudflare.com/sign-up
2. 输入邮箱、设置密码
3. 验证邮箱
4. ✅ 登录成功

### 第3步：下载项目源码

1. 下载 `telegram-poker-bot.zip`
2. 解压到电脑任意位置，记住解压后的文件夹位置

---

## ⚡ 第1部分：部署 Worker 后端（Cloudflare 网页）

### 步骤1：创建 Worker 项目

1. 打开 Cloudflare Dashboard：https://dash.cloudflare.com/
2. 点击左侧菜单 **Workers & Pages**
3. 点击 **Create application**
4. 选择 **Create Worker** 标签
5. 名字随便填（比如 `poker-bot`）
6. 点击 **Deploy**
   > 💡 先部署默认代码没关系，后面我们会替换

### 步骤2：创建 KV 存储（存游戏房间）

1. 现在你在 Worker 详情页
2. 点击左侧菜单 **KV**（在Settings下面）
3. 点击 **Create a namespace**
4. Namespace name 填：`ROOMS`
5. 点击 **Add**

### 步骤3：绑定 KV 到 Worker

1. 回到 Worker 详情页
2. 点击 **Settings** 标签
3. 点击左侧 **Variables**
4. 往下滚动找到 **KV Namespace Bindings**
5. 点击 **Add binding**
6. 填写：
   - **Variable name**: `ROOMS`
   - **KV namespace**: 选择刚才创建的 `ROOMS`
7. 点击 **Save and deploy**

### 步骤4：设置环境变量

1. 还是在 **Settings → Variables** 页面
2. 找到 **Environment Variables**
3. 点击 **Add variable**，依次添加这3个：

| 变量名 | 填什么 |
|--------|--------|
| `TELEGRAM_BOT_TOKEN` | 从 @BotFather 拿到的 Token |
| `WEBHOOK_SECRET` | 随便打30个随机字母（比如 `abc123xyz...`） |
| `TELEGRAM_WEB_APP_URL` | **先空着！第2部分完了再填** |

4. 点击 **Save and deploy**

### 步骤5：上传 Worker 代码

1. 回到 Worker 详情页
2. 点击右上角 **Edit code** 按钮
3. 左边代码编辑器里，**全选删除默认的所有代码**
4. 打开你解压的项目文件夹 → `workers` → `index.js`
5. 全选复制，粘贴到代码编辑器
6. 点击 **Save and deploy**
7. ✅ Worker 部署完成！

### ✅ 记下你的 Worker 域名

在 Worker 详情页，你会看到：
```
https://poker-bot.yourname.workers.dev
```
把这个地址复制保存好！

---

## 🎨 第2部分：部署 Pages 前端（Cloudflare 网页）

> ⭐ **最推荐：方式B - 连接GitHub仓库（自动部署）**
> 
> 方式A适合快速测试，方式B适合长期使用（代码更新自动部署）

---

### 🅰️ 方式A：直接上传文件夹（快速测试）

#### 步骤1：创建 Pages 项目

1. 回到 Cloudflare Dashboard
2. 点击 **Workers & Pages**
3. 点击 **Create application**
4. 选择 **Pages** 标签
5. 点击 **Upload assets**

#### 步骤2：配置并部署

1. **Project name**：随便填（比如 `poker-app`）
2. 点击 **Create project**
3. 点击 **Select folder**
4. 选择你解压的项目 → `frontend` 文件夹
5. ⚠️ **重要：不要点部署！先设置下面的配置**

#### 步骤3：设置构建配置（非常重要！）

1. 往下找到 **Build settings**
2. 设置：
   - **Framework preset**: `None`（不要选Vite！）
   - **Build command**: `npm run build`（或 `cd frontend && npm install && npm run build`）
   - **Build output directory**: `frontend/dist`

#### 步骤4：设置环境变量（必须！）

1. 点击 **Environment variables (advanced)**
2. 点击 **Add variable**，添加：

| 变量名 | 值 |
|--------|-----|
| `PYTHON_VERSION` | `3.12` |
| `NODE_VERSION` | `20` |

#### 步骤5：开始部署

1. 点击 **Save and Deploy**
2. 等待1-2分钟
3. ✅ Pages 部署完成！

---

### 🅱️ 方式B：连接GitHub仓库（⭐ 最推荐！自动部署）

这是**最推荐**的部署方式，后续提交代码自动更新！

#### 3.1 连接GitHub仓库

1. Cloudflare Dashboard → Workers & Pages
2. 点击 **Create application** → **Pages** 标签
3. 点击 **Connect to Git**
4. 选择 **GitHub**，授权Cloudflare访问你的仓库
5. 选择你上传代码的仓库（`telegram-poker-bot`）
6. 点击 **Begin setup**

#### 3.2 构建设置配置（必须完全一致！）

```
Project name:               随便填（比如 poker-bot）
Production branch:          main （或 master，看你的仓库）
Framework preset:           None 【重要！不要选Vue】

Build command:              npm run build
Build output directory:     frontend/dist
Root directory:             （留空，就是 /）
```

#### 3.3 ⚠️ 环境变量（部署前必须添加！）

**点击 Environment variables (advanced)**，添加：

| 变量名 | 值 | 必须 |
|--------|-----|------|
| `PYTHON_VERSION` | `3.12` | ✅ 必须 |
| `NODE_VERSION` | `20` | ✅ 必须 |

> 💡 **为什么需要这个？**
> Cloudflare Pages默认使用最新Python 3.13，会导致构建失败。必须指定3.12版本。

#### 3.4 关于根目录 package.json 的说明

项目根目录的 `package.json` 就是**专门为这种Git连接方式设计的**：
```json
{
  "scripts": {
    "install": "cd frontend && npm install",
    "build": "cd frontend && npm run build"
  }
}
```
- Pages在仓库根目录执行 `npm run build`
- 根目录的脚本自动进入 `frontend/` 子目录执行构建
- 所以你不需要改任何路径配置

#### 3.5 开始部署

点击 **Save and Deploy**，等待3-5分钟。

#### 3.6 部署成功验证

部署完成后：
1. 访问你的Pages域名：`https://xxx.pages.dev`
2. ✅ 应该能看到德州扑克游戏界面
3. ✅ 页面标题显示"Telegram Poker"
4. ❌ 如果显示404或错误，检查：构建输出目录是否是 `frontend/dist`

#### 3.7 后续代码更新

以后只要你push代码到GitHub的main分支，Cloudflare Pages会**自动重新构建部署**！

---

### ✅ 记下你的 Pages 域名

你会看到：
```
https://poker-app.pages.dev
```
把这个地址复制保存好！

---

## 🔧 第3部分：收尾配置（5分钟）

### 步骤1：更新 Worker 配置

1. 回到 Worker 详情页
2. 点击 **Settings → Variables**
3. 找到 `TELEGRAM_WEB_APP_URL`，点击编辑
4. 填入你的 Pages 域名：`https://poker-app.pages.dev`
5. 点击 **Save and deploy**

### 步骤2：设置 Telegram Webhook

> 💡 **不需要命令行！浏览器地址栏直接搞定**

在浏览器地址栏输入（把中文替换成你自己的）：
```
https://api.telegram.org/bot你的TOKEN/setWebhook?url=https://你的Worker域名/webhook&secret_token=你的WEBHOOK_SECRET
```

**完整示例：**
```
https://api.telegram.org/bot1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ1234567890/setWebhook?url=https://poker-bot.yourname.workers.dev/webhook&secret_token=abc123xyz
```

按回车，看到下面这个就成功了：
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

### 步骤3：@BotFather 配置 Web App

回到 Telegram 的 @BotFather：

1. 发送命令：
   ```
   /setdomain
   ```
2. BotFather会让你选Bot，选择你刚创建的
3. 发送你的 Pages 域名：
   ```
   https://poker-app.pages.dev
   ```
4. ✅ 成功！

### （可选）设置菜单按钮

1. 在 @BotFather 发送：
   ```
   /setmenubutton
   ```
2. 选择你的Bot
3. 发送按钮文字：
   ```
   🎮 开始游戏
   ```
4. 发送Pages域名
5. ✅ 现在你的Bot底部有快捷按钮了！

---

## ✅ 第4部分：测试！

1. 在 Telegram 搜索你的Bot（比如 `@MyPokerGameBot`）
2. 发送 `/start`
3. 发送 `/newgame`
4. 点击 **🎴 开始游戏** 按钮
5. ✅ 游戏界面打开了！

---

## 📊 部署完成检查清单

- [ ] @BotFather 创建Bot，拿到Token
- [ ] Cloudflare 账号注册完成
- [ ] Worker 创建完成
- [ ] KV 创建并绑定到Worker
- [ ] Worker 3个环境变量设置完成
- [ ] Worker 代码上传完成
- [ ] Pages 创建并部署完成
- [ ] Worker 更新了 TELEGRAM_WEB_APP_URL
- [ ] Webhook 设置成功
- [ ] @BotFather /setdomain 设置完成
- [ ] Bot 发送 /start 有回复
- [ ] 点击"开始游戏"能打开Web App

---

## ❓ 常见问题

### Q: Pages构建报错 `no such file or directory, open '/.../package.json'`

**错误信息：**
```
npm error Could not read package.json: Error: ENOENT: no such file or directory
```

**原因：** Pages默认在根目录构建，但前端代码在 `frontend/` 子目录

**解决方案：**
1. ✅ 根目录已有 package.json（本项目已修复）
2. ✅ 构建命令填：`npm run build` 或 `cd frontend && npm install && npm run build`
3. ✅ 输出目录填：`frontend/dist`

### Q: Tailwind构建报错 `The 'text-poker-xxx' class does not exist`

**错误信息：**
```
The `text-poker-black` class does not exist. If `text-poker-black` is a custom class, make sure it is defined within a `@layer` directive.
```

**原因：** tailwind.config.js中没有定义poker自定义颜色

**解决方案：**
1. ✅ 项目已修复，tailwind.config.js已添加完整poker颜色定义
2. ✅ 清除浏览器缓存，重新触发Pages部署
3. ✅ 或使用标准Tailwind类：`text-gray-800` 代替 `text-poker-black`

### Q: Pages 构建失败怎么办？

**A:** 检查：
1. Build command 是否正确：`npm run build`
2. Build output directory 是否是 `frontend/dist`
3. 是否设置了 `PYTHON_VERSION=3.12`

### Q: Webhook 设置失败？

**A:** 在浏览器地址栏输入时注意：
1. Token前面有个小写的 `b` 和 `ot`，即 `bot你的TOKEN`
2. Worker域名后面必须加 `/webhook`
3. secret_token 必须和Worker中设置的完全一致

### Q: 点击"开始游戏"没反应？

**A:** 检查：
1. @BotFather 是否执行了 `/setdomain`
2. 域名是否是 HTTPS（Pages自动是HTTPS）
3. Worker中的 TELEGRAM_WEB_APP_URL 是否正确

---

## 🔍 第6章：部署后验证与排错（Bot不响应怎么办？）

### ❌ 问题：发送 /start 或 /newgame 后Bot没反应

这是最常见的问题，按以下步骤逐一排查：

---

#### ✅ 检查1：Worker是否正常运行 + 环境变量检查

**第一步：访问根域名确认运行**
```
https://your-worker.workers.dev
```
**正常应该显示：** `Poker Bot is running! Visit /test for details`

**第二步：访问/test检查所有环境变量（最重要！）**
```
https://your-worker.workers.dev/test
```

**正常应该显示（4个都要是true！）：**
```json
{
  "status": "ok",
  "message": "Worker is running!",
  "env": {
    "hasToken": true,
    "hasSecret": true,
    "hasWebAppUrl": true,
    "hasKV": true
  }
}
```

**❌ 如果任何一个是false：**
- `hasToken: false` → TELEGRAM_BOT_TOKEN 没设置或设置错了
- `hasSecret: false` → WEBHOOK_SECRET 没设置
- `hasWebAppUrl: false` → TELEGRAM_WEB_APP_URL 没设置
- `hasKV: false` → ROOMS KV命名空间没绑定

**如果显示错误/404：**
- Worker代码上传错误
- 重新进入Worker → Edit code → 重新粘贴 `workers/index.js` 代码
- 点击 Save and deploy

---

#### ✅ 检查2：Webhook是否正确设置

在浏览器地址栏访问（替换你的TOKEN）：
```
https://api.telegram.org/bot<你的TOKEN>/getWebhookInfo
```

**正常应该显示：**
```json
{
  "ok": true,
  "result": {
    "url": "https://your-worker.workers.dev/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "last_error_date": null,
    "last_error_message": null
  }
}
```

**异常情况及修复：**
1. ❌ `url` 为空或不对 → 重新设置Webhook
2. ❌ `last_error_date` 有值 → 看 `last_error_message` 错误信息
3. ❌ 显示401 Unauthorized → TOKEN填错了

---

#### ✅ 检查3：重新设置Webhook（90%的问题这样解决！）

在浏览器地址栏访问（全部替换成你自己的）：
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<WORKER域名>/webhook&secret_token=<WEBHOOK_SECRET>
```

**完整示例：**
```
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/setWebhook?url=https://poker-bot.abc.workers.dev/webhook&secret_token=mysecret123
```

看到 `{"ok":true}` 就是成功了！

---

#### ✅ 检查4：Worker环境变量是否正确

Worker详情页 → Settings → Variables：
- ✅ `TELEGRAM_BOT_TOKEN` = 你的Bot Token（从@BotFather来的）
- ✅ `WEBHOOK_SECRET` = 和设置Webhook时的secret_token一样
- ✅ `TELEGRAM_WEB_APP_URL` = 你的Pages域名 `https://xxx.pages.dev`

> ⚠️ **注意：** 环境变量修改后必须点击 **Save and deploy**！

---

#### ✅ 检查5：KV命名空间是否绑定

Worker详情页 → Settings → Variables → 往下拉到 KV Namespace Bindings：
- ✅ 有一个 `ROOMS` 变量
- ✅ 绑定到你创建的KV命名空间

如果没有：点击 Add binding → Variable name填 `ROOMS` → 选择你的KV命名空间 → Save and deploy

---

#### ✅ 检查6：查看Worker实时日志（终极排查）

1. Worker详情页 → Logs → Begin log stream
2. 打开Telegram给Bot发一条消息 `/start`
3. 看日志里有没有请求进来

**如果日志里什么都没有：**
→ Webhook设置错了，Telegram根本没发请求过来

**如果日志里有错误：**
→ 看具体错误信息，通常是：
- TOKEN错误
- KV没绑定
- 代码语法错误

---

### 📋 Bot不响应排查清单

- [ ] Worker域名能访问，显示 "Poker Bot is running!"
- [ ] getWebhookInfo 显示正确的url
- [ ] Webhook的secret_token和Worker环境变量一致
- [ ] Worker三个环境变量都正确配置
- [ ] ROOMS KV已绑定
- [ ] 环境变量修改后已重新部署

---

## 🎉 恭喜！

你已经拥有了一个完整的 Telegram 德州扑克 Bot！

**全程没有：**
- ❌ 命令行输入
- ❌ git操作
- ❌ 编程知识

**只有：**
- ✅ 复制粘贴
- ✅ 点击按钮
- ✅ 填写文本框

分享给你的朋友们一起玩吧！🎰
