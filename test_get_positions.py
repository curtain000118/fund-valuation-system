"""
测试获取持仓API
"""
import requests
import json

url = 'http://localhost:5000/api/positions'

print("测试获取持仓API")
print("=" * 60)

try:
    response = requests.get(url, timeout=30)
    print(f"状态码: {response.status_code}")
    
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"请求失败: {e}")
