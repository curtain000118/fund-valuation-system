"""
检查基金净值数据准确性
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from services.data_fetcher import FundDataFetcher

fetcher = FundDataFetcher()

funds = ['025646', '021315', '022385', '501029']

print("检查基金净值数据")
print("=" * 80)

for code in funds:
    print(f"\n基金代码: {code}")
    print("-" * 40)
    
    info = fetcher.get_fund_info(code)
    if info:
        print(f"  基金名称: {info.get('fund_name', 'N/A')}")
        print(f"  单位净值: {info.get('unit_net_value', 'N/A')}")
        print(f"  估值: {info.get('estimated_value', 'N/A')}")
        print(f"  估值涨跌幅: {info.get('estimated_growth_rate', 'N/A')}%")
        print(f"  净值日期: {info.get('date', 'N/A')}")
        print(f"  估值时间: {info.get('estimated_time', 'N/A')}")
    else:
        print("  无法获取基金信息")
