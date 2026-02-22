"""
清理数据库中的重复持仓数据
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from app import create_app, db
from models import Fund, UserPosition

app = create_app()

with app.app_context():
    print("清理重复持仓数据")
    print("=" * 60)
    
    positions = UserPosition.query.all()
    print(f"当前持仓数量: {len(positions)}")
    
    # 按基金代码分组
    fund_positions = {}
    for pos in positions:
        fund = db.session.get(Fund, pos.fund_id)
        if fund:
            code = fund.fund_code
            if code not in fund_positions:
                fund_positions[code] = []
            fund_positions[code].append(pos)
    
    print("\n各基金持仓数量:")
    for code, pos_list in fund_positions.items():
        fund = db.session.get(Fund, pos_list[0].fund_id)
        print(f"  {code} ({fund.fund_name}): {len(pos_list)}条")
    
    # 删除重复的501029持仓，只保留一条
    if '501029' in fund_positions and len(fund_positions['501029']) > 1:
        print(f"\n发现501029基金有{len(fund_positions['501029'])}条重复记录")
        print("将只保留ID最小的那一条...")
        
        # 按ID排序，保留最小的
        sorted_positions = sorted(fund_positions['501029'], key=lambda x: x.id)
        keep_pos = sorted_positions[0]
        delete_positions = sorted_positions[1:]
        
        print(f"保留: ID={keep_pos.id} ({keep_pos.shares}份 @ {keep_pos.cost_price})")
        
        for pos in delete_positions:
            print(f"删除: ID={pos.id} ({pos.shares}份 @ {pos.cost_price})")
            db.session.delete(pos)
        
        db.session.commit()
        print(f"\n已删除 {len(delete_positions)} 条重复记录")
    
    # 显示清理后的结果
    print("\n清理后的持仓数据:")
    positions = UserPosition.query.all()
    for pos in positions:
        fund = db.session.get(Fund, pos.fund_id)
        print(f"  ID={pos.id}: {fund.fund_code if fund else 'N/A'} - {fund.fund_name if fund else 'N/A'} ({pos.shares}份 @ {pos.cost_price})")
    
    print(f"\n当前总持仓数量: {len(positions)}")
