"""
检查数据库中的持仓数据
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from app import create_app, db
from models import Fund, UserPosition

app = create_app()

with app.app_context():
    print("检查数据库中的持仓数据")
    print("=" * 60)
    
    positions = UserPosition.query.all()
    print(f"总持仓数量: {len(positions)}")
    
    for pos in positions:
        fund = Fund.query.get(pos.fund_id)
        print(f"\n持仓ID: {pos.id}")
        print(f"  基金代码: {fund.fund_code if fund else 'N/A'}")
        print(f"  基金名称: {fund.fund_name if fund else 'N/A'}")
        print(f"  份额: {pos.shares}")
        print(f"  成本价: {pos.cost_price}")
        print(f"  购买日期: {pos.purchase_date}")
