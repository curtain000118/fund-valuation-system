"""
基金实时估值系统 - 主启动文件
"""
import os
from app import create_app, db
from models import Fund, FundNetValue, UserPosition, FundAlert

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Fund': Fund,
        'FundNetValue': FundNetValue,
        'UserPosition': UserPosition,
        'FundAlert': FundAlert
    }

@app.cli.command()
def init_db():
    """初始化数据库"""
    db.create_all()
    print('数据库初始化完成！')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    ssl_dir = os.path.join(os.path.dirname(__file__), 'ssl')
    cert_path = os.path.join(ssl_dir, 'cert.pem')
    key_path = os.path.join(ssl_dir, 'key.pem')
    
    use_ssl = os.environ.get('USE_SSL', '').lower() == 'true'
    
    print('=' * 60)
    print('基金实时估值系统启动成功！')
    print('=' * 60)
    
    if use_ssl:
        print('访问地址: https://localhost:5000')
        print('SSL证书: 已启用')
    else:
        print('访问地址: http://localhost:5000')
        print('SSL证书: 未启用 (设置环境变量 USE_SSL=true 启用)')
    
    print('功能说明:')
    print('  - 首页: 基金搜索和排行')
    print('  - 持仓管理: 管理您的基金持仓')
    print('  - 预警提醒: 设置涨跌幅预警')
    print('  - 数据分析: 定投计算和基金对比')
    print('=' * 60)
    print('提示: 代码修改后自动重载，无需手动重启')
    print('=' * 60)
    
    ssl_context = None
    if use_ssl:
        ssl_context = 'adhoc'
    
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000, 
        use_reloader=True, 
        extra_files=['config.py'],
        ssl_context=ssl_context
    )
