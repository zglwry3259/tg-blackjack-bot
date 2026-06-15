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

### 步骤1：创建 Pages 项目

1. 回到 Cloudflare Dashboard
2. 点击 **Workers & Pages**
3. 点击 **Create application**
4. 选择 **Pages** 标签
5. 点击 **Upload assets**

### 步骤2：配置并部署

1. **Project name**：随便填（比如 `poker-app`）
2. 点击 **Create project**
3. 点击 **Select folder**
4. 选择你解压的项目 → `frontend` 文件夹
5. ⚠️ **重要：不要点部署！先设置下面的配置**

### 步骤3：设置构建配置（非常重要！）

1. 往下找到 **Build settings**
2. 设置：
   - **Framework preset**: `None`（不要选Vite！）
   - **Build command**: `npm run build`（或 `cd frontend && npm install && npm run build`）
   - **Build output directory**: `frontend/dist`

### 步骤4：设置环境变量（必须！）

1. 点击 **Environment variables (advanced)**
2. 点击 **Add variable**，添加：

| 变量名 | 值 |
|--------|-----|
| `PYTHON_VERSION` | `3.12` |
| `NODE_VERSION` | `20` |

### 步骤5：开始部署

1. 点击 **Save and Deploy**
2. 等待1-2分钟
3. ✅ Pages 部署完成！

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
