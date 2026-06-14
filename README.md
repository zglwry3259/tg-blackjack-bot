# 🃏 TG Blackjack Bot — Cloudflare Pages 联机21点

> 部署在 **Cloudflare Pages** 上的 **Telegram Bot**，支持多人联机对战 21点（Blackjack）游戏。
> 通过 **Telegram Mini App（小程序）** 提供游戏界面，使用 **Durable Objects + WebSocket** 实现实时联机。

## ✨ 功能特性

- 🎮 **完整21点游戏**：标准规则 + Blackjack 加成奖励
- 👥 **多人联机**：最多 5 人同时在线对战（WebSocket 实时同步）
- 📱 **Telegram Mini App**：点击按钮直接打开游戏，无需离开 Telegram
- 💬 **房间聊天**：游戏中可实时文字交流
- 🔗 **邀请链接**：一键分享房间给好友
- 🎨 **精美 UI**：扑克牌动画、响应式设计、深色主题
- ☁️ **零服务器成本**：完全运行在 Cloudflare 免费额度内

## 🚀 一键部署（GitHub Actions）

本项目已配置 **GitHub Actions 自动部署**，推送代码到 main 分支即可自动部署！

### 配置 Secrets：
仓库 → **Settings → Secrets and variables → Actions → New repository secret**

| Secret 名 | 值 | 获取方式 |
|-----------|-----|----------|
| `CLOUDFLARE_API_TOKEN` | CF API Token | Dashboard → My Profile → API Tokens → Create Token |
| `CLOUDFLARE_ACCOUNT_ID` | Account ID | CF Dashboard 右侧栏 → API |

### 手动触发：
仓库 → **Actions → Deploy to Cloudflare Pages → Run workflow**

## 📋 游戏规则

- A = 1或11点，J/Q/K = 10点
- Hit要牌 / Stand停牌
- >21爆牌输，Blackjack前两张=21大赢
- 庄家<17必须要，≥17停牌

MIT License
