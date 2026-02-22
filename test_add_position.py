"""
测试添加持仓API
"""
import requests
import json

url = 'http://localhost:5000/api/positions'

data = {
    'fund_code': '000001',
    'shares': 1000.0,
    'cost_price': 1.15,
    'purchase_date': '2024-01-01'
}

print("测试添加持仓API")
print("=" * 60)
print(f"请求URL: {url}")
print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")

try:
    response = requests.post(url, json=data, timeout=10)
    print(f"\n状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"\n请求失败: {e}")
