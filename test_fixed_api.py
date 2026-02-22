"""
测试修复后的数据获取功能
"""
from services.data_fetcher import FundDataFetcher

fetcher = FundDataFetcher()

print("=" * 60)
print("测试基金搜索")
print("=" * 60)
funds = fetcher.search_fund('000001')
print(f"搜索结果数量: {len(funds)}")
for fund in funds:
    print(f"  {fund['fund_code']} - {fund['fund_name']} ({fund['fund_type']})")

print("\n" + "=" * 60)
print("测试基金信息获取")
print("=" * 60)
info = fetcher.get_fund_info('000001')
if info:
    print(f"基金代码: {info['fund_code']}")
    print(f"基金名称: {info['fund_name']}")
    print(f"单位净值: {info['unit_net_value']}")
    print(f"估算净值: {info['estimated_value']}")
    print(f"估算涨跌: {info['estimated_growth_rate']}%")
else:
    print("获取失败")

print("\n" + "=" * 60)
print("测试基金排行")
print("=" * 60)
rank = fetcher.get_fund_rank('all', 'zzf', 'desc', 1, 5)
print(f"排行数量: {len(rank)}")
for fund in rank:
    print(f"  {fund['fund_code']} - {fund['fund_name']} | 净值: {fund['unit_net_value']} | 涨跌: {fund['daily_growth_rate']}%")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
