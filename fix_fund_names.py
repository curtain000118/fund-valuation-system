"""
检查并修复数据库中的基金名称
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from app import create_app, db
from models import Fund, UserPosition
from services.data_fetcher import FundDataFetcher

fetcher = FundDataFetcher()
app = create_app()

with app.app_context():
    print("检查数据库中的基金记录")
    print("=" * 60)
    
    funds = Fund.query.all()
    
    for fund in funds:
        print(f"\n基金ID: {fund.id}")
        print(f"  代码: {fund.fund_code}")
        print(f"  名称: {fund.fund_name or '(空)'}")
        print(f"  类型: {fund.fund_type or '(空)'}")
        
        if not fund.fund_name:
            print("  -> 正在获取基金信息...")
            fund_info = fetcher.get_fund_info(fund.fund_code)
            
            if fund_info:
                fund.fund_name = fund_info.get('fund_name', '')
                fund.fund_type = fund_info.get('fund_type', '')
                print(f"  -> 更新名称: {fund.fund_name}")
                print(f"  -> 更新类型: {fund.fund_type}")
            else:
                print("  -> 无法获取基金信息")
    
    db.session.commit()
    print("\n数据库更新完成！")
