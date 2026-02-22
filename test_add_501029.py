"""
测试添加501029基金
"""
import requests
import json

url = 'http://localhost:5000/api/positions'

data = {
    'fund_code': '501029',
    'shares': 100,
    'cost_price': 1.5,
    'purchase_date': '2024-01-01'
}

print("测试添加501029基金")
print("=" * 60)
print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"请求失败: {e}")
