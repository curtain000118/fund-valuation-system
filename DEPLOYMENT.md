# Vercel 部署指南

本文档详细说明如何将基金实时估值系统部署到 Vercel 平台。

## 📋 前置要求

1. **Vercel 账号** - [注册 Vercel 账号](https://vercel.com/signup)
2. **GitHub 账号** - 用于代码托管和自动部署
3. **Git** - 本地安装 Git

## 🚀 快速部署

### 步骤 1: 准备代码仓库

```bash
# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "准备部署到 Vercel"

# 推送到 GitHub
git remote add origin https://github.com/your-username/fund-valuation-system.git
git push -u origin main
```

### 步骤 2: 在 Vercel 创建项目

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 **"New Project"**
3. 导入你的 GitHub 仓库
4. 选择 `fund-valuation-system` 仓库

### 步骤 3: 配置项目

**Framework Preset:** Other

**Build & Development Settings:**
- Build Command: 留空（Vercel 自动检测）
- Output Directory: 留空
- Install Command: `pip install -r requirements-vercel.txt`

**Root Directory:** `./`（默认）

### 步骤 4: 配置环境变量

在 Vercel 项目设置中添加以下环境变量：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `SECRET_KEY` | Flask 密钥 | `your-secret-key-here` |
| `TUSHARE_TOKEN` | Tushare API Token（可选） | `your-tushare-token` |

### 步骤 5: 配置数据库

#### 方案 A: 使用 Vercel Postgres（推荐）

1. 在 Vercel 项目中，进入 **Storage** 标签
2. 点击 **"Create Database"**
3. 选择 **"Postgres"**
4. 数据库创建后，Vercel 会自动注入以下环境变量：
   - `POSTGRES_URL`
   - `POSTGRES_PRISMA_URL`
   - `POSTGRES_URL_NON_POOLING`

#### 方案 B: 使用其他云数据库

**Supabase:**
1. 访问 [Supabase](https://supabase.com)
2. 创建新项目
3. 获取数据库连接字符串
4. 在 Vercel 中添加环境变量 `DATABASE_URL`

**PlanetScale:**
1. 访问 [PlanetScale](https://planetscale.com)
2. 创建数据库
3. 获取连接字符串
4. 在 Vercel 中添加环境变量 `DATABASE_URL`

### 步骤 6: 部署

点击 **"Deploy"** 按钮，等待部署完成。

## 📊 数据库迁移

如果你有现有的 SQLite 数据需要迁移：

### 方法 1: 使用迁移脚本

```bash
# 本地运行迁移脚本
python scripts/migrate_to_postgres.py --sqlite-path instance/fund_system.db
```

### 方法 2: 手动导出导入

```bash
# 导出 SQLite 数据
sqlite3 instance/fund_system.db .dump > backup.sql

# 使用 Vercel CLI 连接数据库
vercel env pull .env.local

# 导入到 PostgreSQL
psql $DATABASE_URL < backup.sql
```

## ⏰ 配置定时任务

项目已配置 Vercel Cron Jobs，用于定时更新基金数据：

- **触发时间**: 每个工作日的 9:00 和 15:00
- **执行路径**: `/api/cron/update-funds`
- **配置文件**: `vercel.json`

修改定时任务配置：

```json
{
  "crons": [
    {
      "path": "/api/cron/update-funds",
      "schedule": "0 9,15 * * 1-5"
    }
  ]
}
```

Cron 表达式说明：
- `0 9,15 * * 1-5` = 每周一到周五的 9:00 和 15:00
- `*/30 * * * *` = 每 30 分钟
- `0 0 * * *` = 每天午夜

## 🔧 本地开发

### 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实际值
```

### 运行应用

```bash
python run.py
```

访问 http://localhost:5000

## 📁 项目结构

```
fund-valuation-system/
├── api/                    # Vercel Serverless Functions
│   ├── index.py           # 主入口
│   └── cron.py            # 定时任务
├── routes/                # Flask 路由
│   ├── main.py           # 页面路由
│   └── api.py            # API 路由
├── services/              # 业务逻辑
│   ├── data_fetcher.py   # 数据获取
│   └── valuation_engine.py # 估值引擎
├── templates/             # Jinja2 模板
├── scripts/               # 工具脚本
│   ├── migrate_to_postgres.py
│   └── init_db.py
├── app.py                 # Flask 应用
├── config.py              # 配置文件
├── models.py              # 数据模型
├── vercel.json            # Vercel 配置
├── requirements-vercel.txt # Vercel 依赖
└── .vercelignore          # Vercel 忽略文件
```

## 🐛 常见问题

### 1. 数据库连接失败

**问题**: `could not connect to server: Connection refused`

**解决方案**:
- 检查 `DATABASE_URL` 环境变量是否正确
- 确认数据库服务是否运行
- 检查防火墙设置

### 2. 函数执行超时

**问题**: `Function execution timed out`

**解决方案**:
- 在 `vercel.json` 中增加 `maxDuration`
- 优化代码执行效率
- 升级到 Pro 计划（最长 60 秒）

### 3. 静态文件加载失败

**问题**: CSS/JS 文件 404

**解决方案**:
- 确保模板中正确引用静态文件
- 检查文件路径是否正确

### 4. 环境变量未生效

**问题**: 环境变量读取不到

**解决方案**:
- 在 Vercel Dashboard 中确认环境变量已添加
- 重新部署项目
- 检查环境变量名称是否正确

## 💰 成本估算

### Vercel Hobby 计划（免费）

- ✅ 无限部署
- ✅ 100GB 带宽/月
- ✅ 100GB 函数执行/月
- ✅ 1 个团队项目
- ⚠️ 函数最长执行 10 秒
- ⚠️ Cron Jobs 限制

### Vercel Pro 计划（$20/月）

- ✅ 无限团队项目
- ✅ 1TB 带宽/月
- ✅ 函数最长执行 60 秒
- ✅ 更多 Cron Jobs

### 数据库成本

- **Vercel Postgres**: 免费额度足够小型应用
- **Supabase**: 免费计划 500MB
- **PlanetScale**: 免费计划 5GB

## 🔐 安全建议

1. **密钥管理**
   - 使用强随机密钥
   - 定期轮换密钥
   - 不要在代码中硬编码

2. **数据库安全**
   - 使用 SSL 连接
   - 限制数据库访问 IP
   - 定期备份

3. **API 安全**
   - 添加请求频率限制
   - 验证用户输入
   - 使用 HTTPS

## 📈 性能优化

1. **数据库优化**
   - 添加索引
   - 使用连接池
   - 优化查询语句

2. **缓存策略**
   - 使用 Vercel Edge Cache
   - 实现应用层缓存
   - 静态资源 CDN

3. **函数优化**
   - 减少冷启动时间
   - 优化依赖大小
   - 使用懒加载

## 🆕 后续优化建议

### 短期优化（1-2 周）

1. **添加 Redis 缓存**
   - 缓存基金数据
   - 减少数据库查询
   - 提升响应速度

2. **实现用户认证**
   - 添加登录/注册功能
   - 使用 JWT Token
   - 保护用户数据

3. **添加监控告警**
   - 集成 Sentry 错误追踪
   - 添加性能监控
   - 设置告警规则

### 中期优化（1-2 月）

1. **API 优化**
   - 添加 GraphQL 支持
   - 实现 API 限流
   - 添加 API 文档

2. **前端优化**
   - 迁移到 React/Vue
   - 实现 SSR
   - 优化加载速度

3. **数据同步优化**
   - 实现增量更新
   - 添加消息队列
   - 优化定时任务

### 长期优化（3-6 月）

1. **微服务架构**
   - 拆分服务
   - 使用容器化
   - 实现服务发现

2. **多区域部署**
   - 使用 CDN
   - 实现就近访问
   - 提升全球访问速度

3. **数据分析**
   - 添加数据仓库
   - 实现数据可视化
   - AI 预测分析

## 📞 获取帮助

- **Vercel 文档**: https://vercel.com/docs
- **Flask 文档**: https://flask.palletsprojects.com/
- **项目 Issues**: https://github.com/your-username/fund-valuation-system/issues

---

**祝你部署顺利！** 🎉
