"""
测试前端添加持仓流程
"""
import requests
import json

# 测试添加501029基金
url = 'http://localhost:5000/api/positions'

data = {
    'fund_code': '501029',
    'shares': 100,
    'cost_price': 1.5,
    'purchase_date': '2024-01-01'
}

print("测试添加501029基金")
print("=" * 60)

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✅ 添加成功！")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # 检查持仓列表
        print("\n检查持仓列表...")
        get_response = requests.get(url, timeout=30)
        positions = get_response.json()
        print(f"当前持仓数量: {len(positions.get('positions', []))}")
        
        # 查找501029基金
        for pos in positions.get('positions', []):
            if pos['fund_code'] == '501029':
                print(f"✅ 找到501029基金持仓: {pos}")
                break
        else:
            print("❌ 未找到501029基金持仓")
    else:
        print(f"❌ 添加失败: {response.text}")
        
except Exception as e:
    print(f"❌ 请求失败: {e}")
