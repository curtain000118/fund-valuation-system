# 基金实时估值系统

一个基于 Flask 的基金实时估值系统，支持基金搜索、实时估值、持仓管理、预警提醒等功能。

## 功能特性

### 1. 基金搜索与排行
- 支持按基金代码或名称搜索
- 查看热门基金排行
- 按基金类型筛选（股票型、混合型、债券型等）

### 2. 实时估值
- 获取基金实时估值数据
- 显示估算净值和涨跌幅
- 查看历史净值走势图

### 3. 持仓管理
- 添加、编辑、删除持仓
- 自动计算持仓市值和收益
- 查看投资组合总览

### 4. 预警提醒
- 设置涨跌幅预警
- 支持多只基金预警
- 预警触发通知

### 5. 数据分析
- 定投收益计算器
- 基金对比分析
- 收益率统计

## 技术栈

- **后端**: Flask 3.0
- **数据库**: SQLite (可切换到 PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **前端**: Bootstrap 5 + Chart.js
- **数据源**: 天天基金/东方财富

## 安装步骤

### 1. 创建虚拟环境

```bash
cd d:\py\fund-valuation-system
python -m venv venv
```

### 2. 激活虚拟环境

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:
```cmd
.\venv\Scripts\activate.bat
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
python run.py
```

首次运行会自动创建数据库。

## 使用方法

### 启动服务

```bash
python run.py
```

### 访问系统

打开浏览器访问: http://localhost:5000

## 项目结构

```
fund-valuation-system/
├── app.py                  # Flask应用初始化
├── config.py               # 配置文件
├── models.py               # 数据模型
├── run.py                  # 启动文件
├── requirements.txt        # 依赖列表
├── routes/                 # 路由模块
│   ├── __init__.py
│   ├── main.py            # 页面路由
│   └── api.py             # API路由
├── services/               # 服务模块
│   ├── __init__.py
│   ├── data_fetcher.py    # 数据获取
│   └── valuation_engine.py # 估值计算
└── templates/              # HTML模板
    ├── index.html         # 首页
    ├── portfolio.html     # 持仓管理
    ├── alerts.html        # 预警提醒
    ├── analysis.html      # 数据分析
    └── fund_detail.html   # 基金详情
```

## API 接口

### 基金相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/funds/search?keyword=xxx` | GET | 搜索基金 |
| `/api/funds/<fund_code>` | GET | 获取基金信息 |
| `/api/funds/<fund_code>/valuation` | GET | 获取实时估值 |
| `/api/funds/<fund_code>/net-values` | GET | 获取历史净值 |
| `/api/funds/rank` | GET | 获取基金排行 |

### 持仓相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/positions` | GET | 获取所有持仓 |
| `/api/positions` | POST | 添加持仓 |
| `/api/positions/<id>` | PUT | 更新持仓 |
| `/api/positions/<id>` | DELETE | 删除持仓 |

### 预警相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/alerts` | GET | 获取所有预警 |
| `/api/alerts` | POST | 添加预警 |
| `/api/alerts/<id>` | DELETE | 删除预警 |

## 配置说明

在 `config.py` 中可以修改以下配置：

```python
class Config:
    SECRET_KEY = 'your-secret-key'  # 密钥
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fund_system.db'  # 数据库
    UPDATE_INTERVAL = 60  # 更新间隔（秒）
    ALERT_THRESHOLD_UP = 5.0  # 上涨预警阈值
    ALERT_THRESHOLD_DOWN = -5.0  # 下跌预警阈值
```

## 注意事项

1. **数据来源**: 本系统使用天天基金/东方财富的公开数据接口，请合理使用，避免频繁请求。

2. **估值时间**: 基金实时估值仅在交易日的交易时间（9:30-15:00）更新，非交易时间显示的是最近一次估值。

3. **数据准确性**: 估值数据仅供参考，实际净值以基金公司公布为准。

4. **生产环境**: 部署到生产环境时，建议：
   - 使用 PostgreSQL 或 MySQL 替代 SQLite
   - 配置 HTTPS
   - 设置适当的 SECRET_KEY
   - 关闭 DEBUG 模式

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue。
