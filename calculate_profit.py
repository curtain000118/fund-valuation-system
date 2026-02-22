"""
计算收益对比
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from app import create_app, db
from models import Fund, UserPosition
from services.data_fetcher import FundDataFetcher

app = create_app()
fetcher = FundDataFetcher()

with app.app_context():
    print("收益计算对比")
    print("=" * 80)
    
    positions = UserPosition.query.all()
    
    for pos in positions:
        fund = db.session.get(Fund, pos.fund_id)
        info = fetcher.get_fund_info(fund.fund_code)
        
        print(f"\n基金: {fund.fund_code} - {fund.fund_name}")
        print("-" * 60)
        print(f"  份额: {pos.shares}")
        print(f"  成本价: {pos.cost_price}")
        print(f"  成本总额: {pos.shares * pos.cost_price:.2f}")
        
        if info:
            net_value = info.get('unit_net_value')
            estimated_value = info.get('estimated_value')
            
            print(f"  最新净值: {net_value} (日期: {info.get('date')})")
            print(f"  估值: {estimated_value}")
            
            if net_value:
                market_value = pos.shares * net_value
                profit = market_value - pos.shares * pos.cost_price
                profit_rate = profit / (pos.shares * pos.cost_price) * 100
                
                print(f"  按净值计算:")
                print(f"    市值: {market_value:.2f}")
                print(f"    收益: {profit:.2f}")
                print(f"    收益率: {profit_rate:.2f}%")
            
            if estimated_value:
                est_market_value = pos.shares * estimated_value
                est_profit = est_market_value - pos.shares * pos.cost_price
                est_profit_rate = est_profit / (pos.shares * pos.cost_price) * 100
                
                print(f"  按估值计算:")
                print(f"    市值: {est_market_value:.2f}")
                print(f"    收益: {est_profit:.2f}")
                print(f"    收益率: {est_profit_rate:.2f}%")
        else:
            print("  无法获取净值数据")
