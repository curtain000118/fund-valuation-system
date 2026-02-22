"""
清理数据库中的持仓数据
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from app import create_app, db
from models import Fund, UserPosition

app = create_app()

with app.app_context():
    print("当前数据库中的持仓数据:")
    print("=" * 60)
    
    positions = UserPosition.query.all()
    print(f"总持仓数量: {len(positions)}")
    
    for pos in positions:
        fund = db.session.get(Fund, pos.fund_id)
        print(f"  ID={pos.id}: {fund.fund_code if fund else 'N/A'} - {fund.fund_name if fund else 'N/A'} ({pos.shares}份 @ {pos.cost_price})")
    
    print("\n" + "=" * 60)
    print("请选择操作:")
    print("1. 删除所有持仓数据")
    print("2. 删除指定ID的持仓")
    print("3. 保留指定ID的持仓，删除其他")
    print("4. 取消")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == '1':
        confirm = input("确认删除所有持仓数据? (yes/no): ").strip().lower()
        if confirm == 'yes':
            num_deleted = UserPosition.query.delete()
            db.session.commit()
            print(f"已删除 {num_deleted} 条持仓记录")
        else:
            print("已取消")
    
    elif choice == '2':
        ids = input("请输入要删除的持仓ID (用逗号分隔): ").strip()
        ids_list = [int(id.strip()) for id in ids.split(',') if id.strip().isdigit()]
        
        if ids_list:
            confirm = input(f"确认删除ID为 {ids_list} 的持仓? (yes/no): ").strip().lower()
            if confirm == 'yes':
                for id in ids_list:
                    pos = db.session.get(UserPosition, id)
                    if pos:
                        db.session.delete(pos)
                db.session.commit()
                print(f"已删除 {len(ids_list)} 条持仓记录")
            else:
                print("已取消")
        else:
            print("无效的ID")
    
    elif choice == '3':
        ids = input("请输入要保留的持仓ID (用逗号分隔): ").strip()
        ids_list = [int(id.strip()) for id in ids.split(',') if id.strip().isdigit()]
        
        if ids_list:
            confirm = input(f"确认只保留ID为 {ids_list} 的持仓，删除其他所有? (yes/no): ").strip().lower()
            if confirm == 'yes':
                positions_to_delete = UserPosition.query.filter(~UserPosition.id.in_(ids_list)).all()
                for pos in positions_to_delete:
                    db.session.delete(pos)
                db.session.commit()
                print(f"已删除 {len(positions_to_delete)} 条持仓记录")
            else:
                print("已取消")
        else:
            print("无效的ID")
    
    else:
        print("已取消")
    
    print("\n清理完成!")
