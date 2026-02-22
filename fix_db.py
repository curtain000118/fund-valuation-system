"""
修复数据库数据
"""
from app import create_app, db
from models import Fund, UserPosition
from services.data_fetcher import FundDataFetcher

app = create_app('development')
fetcher = FundDataFetcher()

with app.app_context():
    positions = UserPosition.query.all()
    
    for pos in positions:
        fund = Fund.query.get(pos.fund_id)
        
        if not fund:
            print(f"删除无效持仓: ID={pos.id}, 基金ID={pos.fund_id} 不存在")
            db.session.delete(pos)
        else:
            if not fund.fund_name:
                fund_info = fetcher.get_fund_info(fund.fund_code)
                if fund_info:
                    fund.fund_name = fund_info.get('fund_name', '')
                    print(f"更新基金名称: {fund.fund_code} -> {fund.fund_name}")
    
    db.session.commit()
    print("\n数据库修复完成！")
    
    print("\n" + "=" * 60)
    print("修复后的数据:")
    print("=" * 60)
    
    funds = Fund.query.all()
    for fund in funds:
        print(f"  基金: {fund.fund_code} - {fund.fund_name}")
    
    positions = UserPosition.query.all()
    for pos in positions:
        fund = Fund.query.get(pos.fund_id)
        print(f"  持仓: {fund.fund_code if fund else 'N/A'} - {pos.shares}份")
