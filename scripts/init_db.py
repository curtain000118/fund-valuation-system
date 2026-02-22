"""
数据库初始化脚本 - 支持 PostgreSQL
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models import Fund, FundNetValue, UserPosition, FundAlert

def init_database():
    """
    初始化数据库
    """
    app = create_app()
    
    with app.app_context():
        try:
            print("开始初始化数据库...")
            
            db.create_all()
            print("✓ 数据库表创建完成")
            
            print("\n数据库表结构:")
            print("  - fund: 基金基本信息表")
            print("  - fund_net_value: 基金净值表")
            print("  - user_position: 用户持仓表")
            print("  - fund_alert: 基金预警表")
            
            print("\n✅ 数据库初始化完成！")
            return True
            
        except Exception as e:
            print(f"\n❌ 初始化失败: {str(e)}")
            return False

if __name__ == '__main__':
    init_database()
