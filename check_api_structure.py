"""
检查API返回的数据结构
"""
import requests
import json

url = 'http://localhost:5000/api/positions'

try:
    response = requests.get(url, timeout=30)
    data = response.json()
    
    print("API响应数据结构检查:")
    print("=" * 60)
    
    if 'positions' in data and data['positions']:
        print(f"持仓数量: {len(data['positions'])}")
        
        # 检查第一个持仓的数据结构
        first_position = data['positions'][0]
        print("\n第一个持仓的数据结构:")
        for key, value in first_position.items():
            print(f"  {key}: {value} (类型: {type(value).__name__})")
        
        # 检查是否有 position_id 字段
        if 'position_id' in first_position:
            print("\n✅ position_id 字段存在")
        else:
            print("\n❌ position_id 字段不存在")
            print("  实际字段:", list(first_position.keys()))
    else:
        print("❌ 没有持仓数据")
        
except Exception as e:
    print(f"错误: {e}")
