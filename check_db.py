"""
检查数据库数据
"""
from app import create_app, db
from models import Fund, UserPosition

app = create_app('development')

with app.app_context():
    funds = Fund.query.all()
    print("=" * 60)
    print("数据库中的基金:")
    print("=" * 60)
    for fund in funds:
        print(f"  ID: {fund.id}, 代码: {fund.fund_code}, 名称: {fund.fund_name}")
    
    positions = UserPosition.query.all()
    print("\n" + "=" * 60)
    print("数据库中的持仓:")
    print("=" * 60)
    for pos in positions:
        print(f"  ID: {pos.id}, 基金ID: {pos.fund_id}, 份额: {pos.shares}, 成本: {pos.cost_price}")
