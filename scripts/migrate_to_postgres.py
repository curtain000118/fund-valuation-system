"""
数据库迁移脚本 - 支持 PostgreSQL
用于将 SQLite 数据迁移到 PostgreSQL
"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models import Fund, FundNetValue, UserPosition, FundAlert
import sqlite3

def migrate_from_sqlite_to_postgres(sqlite_path='instance/fund_system.db'):
    """
    从 SQLite 迁移数据到 PostgreSQL
    """
    app = create_app('production')
    
    if not os.path.exists(sqlite_path):
        print(f"SQLite 数据库文件不存在: {sqlite_path}")
        return False
    
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    
    with app.app_context():
        try:
            print("开始迁移数据...")
            
            db.create_all()
            print("✓ PostgreSQL 数据库表创建完成")
            
            cursor.execute("SELECT * FROM fund")
            funds = cursor.fetchall()
            for fund_data in funds:
                fund = Fund(
                    fund_code=fund_data[1],
                    fund_name=fund_data[2],
                    fund_type=fund_data[3],
                    fund_manager=fund_data[4],
                    fund_company=fund_data[5],
                    establish_date=datetime.strptime(fund_data[6], '%Y-%m-%d') if fund_data[6] else None,
                    fund_scale=fund_data[7]
                )
                db.session.add(fund)
            print(f"✓ 迁移 {len(funds)} 条基金数据")
            
            cursor.execute("SELECT * FROM fund_net_value")
            net_values = cursor.fetchall()
            for nv_data in net_values:
                net_value = FundNetValue(
                    fund_code=nv_data[1],
                    date=datetime.strptime(nv_data[2], '%Y-%m-%d').date() if nv_data[2] else None,
                    net_value=nv_data[3],
                    accumulated_value=nv_data[4],
                    daily_growth=nv_data[5]
                )
                db.session.add(net_value)
            print(f"✓ 迁移 {len(net_values)} 条净值数据")
            
            cursor.execute("SELECT * FROM user_position")
            positions = cursor.fetchall()
            for pos_data in positions:
                position = UserPosition(
                    fund_code=pos_data[1],
                    shares=pos_data[2],
                    cost_price=pos_data[3],
                    buy_date=datetime.strptime(pos_data[4], '%Y-%m-%d').date() if pos_data[4] else None,
                    notes=pos_data[5]
                )
                db.session.add(position)
            print(f"✓ 迁移 {len(positions)} 条持仓数据")
            
            cursor.execute("SELECT * FROM fund_alert")
            alerts = cursor.fetchall()
            for alert_data in alerts:
                alert = FundAlert(
                    fund_code=alert_data[1],
                    alert_type=alert_data[2],
                    threshold=alert_data[3],
                    is_active=bool(alert_data[4]),
                    created_at=datetime.strptime(alert_data[5], '%Y-%m-%d %H:%M:%S') if alert_data[5] else None
                )
                db.session.add(alert)
            print(f"✓ 迁移 {len(alerts)} 条预警数据")
            
            db.session.commit()
            print("\n✅ 数据迁移完成！")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"\n❌ 迁移失败: {str(e)}")
            db.session.rollback()
            conn.close()
            return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库迁移工具')
    parser.add_argument('--sqlite-path', default='instance/fund_system.db', help='SQLite 数据库路径')
    
    args = parser.parse_args()
    
    migrate_from_sqlite_to_postgres(args.sqlite_path)
