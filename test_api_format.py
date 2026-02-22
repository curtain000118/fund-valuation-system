"""
测试API返回的数据格式
"""
import requests
import json

url = 'http://localhost:5000/api/positions'

print("测试API返回的数据格式")
print("=" * 60)

try:
    response = requests.get(url, timeout=30)
    print(f"状态码: {response.status_code}")
    
    data = response.json()
    print(f"响应数据结构:")
    print(f"  - 总市值: {data.get('total_market_value', 'N/A')}")
    print(f"  - 总成本: {data.get('total_cost_value', 'N/A')}")
    print(f"  - 总收益: {data.get('total_profit', 'N/A')}")
    print(f"  - 收益率: {data.get('total_profit_rate', 'N/A')}")
    print(f"  - 持仓数量: {len(data.get('positions', []))}")
    
    if 'positions' in data and data['positions']:
        print("\n前3个持仓数据:")
        for i, pos in enumerate(data['positions'][:3]):
            print(f"  {i+1}. 基金代码: {pos.get('fund_code', 'N/A')}")
            print(f"     基金名称: {pos.get('fund_name', 'N/A')}")
            print(f"     持仓ID: {pos.get('position_id', 'N/A')}")
            print(f"     份额: {pos.get('shares', 'N/A')}")
            print(f"     成本价: {pos.get('cost_price', 'N/A')}")
            print(f"     市值: {pos.get('market_value', 'N/A')}")
            print(f"     收益: {pos.get('profit', 'N/A')}")
            print()
    else:
        print("\n⚠️ 持仓数据为空")
        
except Exception as e:
    print(f"请求失败: {e}")
