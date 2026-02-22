import requests
import json

url = 'http://localhost:5000/api/positions'

try:
    response = requests.get(url, timeout=30)
    data = response.json()
    
    print("API响应数据:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"错误: {e}")
