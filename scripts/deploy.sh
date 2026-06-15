#!/bin/bash
# Telegram Poker Bot 部署脚本

set -e

echo "🚀 开始部署 Telegram Poker Bot..."

# 检查 wrangler 是否安装
if ! command -v wrangler &> /dev/null; then
    echo "📦 安装 Wrangler CLI..."
    npm install -g wrangler
fi

# 登录 Cloudflare
echo "🔐 登录 Cloudflare..."
wrangler login

# 创建 D1 数据库
echo "🗄️ 创建 D1 数据库..."
wrangler d1 create telegram-poker-db || true

# 执行数据库迁移
echo "📝 执行数据库迁移..."
wrangler d1 execute telegram-poker-db --file=./workers/schema.sql

# 创建 KV 命名空间
echo "🔑 创建 KV 命名空间..."
wrangler kv:namespace create ROOMS || true

echo ""
echo "✅ 数据库创建完成！"
echo ""
echo "📋 接下来的步骤："
echo "1. 编辑 workers/wrangler.toml 填入数据库ID和KV ID"
echo "2. 配置环境变量"
echo "3. 运行: cd workers && npm run deploy"
echo "4. 部署前端: cd frontend && npm run build && wrangler pages deploy dist"
echo ""
echo "🎉 部署完成！"
