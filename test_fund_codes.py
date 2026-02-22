"""
测试特定基金代码的数据获取
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from services.data_fetcher import FundDataFetcher

fetcher = FundDataFetcher()

test_codes = ['501029', '160221', '019005']

print("测试基金数据获取")
print("=" * 60)

for code in test_codes:
    print(f"\n基金代码: {code}")
    print("-" * 40)
    
    info = fetcher.get_fund_info(code)
    print(f"基金信息: {info}")
    
    detail = fetcher.get_fund_detail(code)
    print(f"基金详情: {detail}")
