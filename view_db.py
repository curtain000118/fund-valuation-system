"""
数据库可视化工具
"""
import sys
sys.path.insert(0, 'd:/py/fund-valuation-system')

from app import create_app, db
from models import Fund, FundNetValue, UserPosition, FundAlert
from datetime import datetime

app = create_app()

def print_table(title, headers, rows):
    """打印表格"""
    print(f"\n{'='*80}")
    print(f" {title}")
    print(f"{'='*80}")
    
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    header_line = ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print('-' * len(header_line))
    
    for row in rows:
        print(' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
    
    print(f"共 {len(rows)} 条记录")

with app.app_context():
    print("\n" + "="*80)
    print(" 基金实时估值系统 - 数据库可视化")
    print(f" 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # 基金表
    funds = Fund.query.all()
    if funds:
        headers = ['ID', '基金代码', '基金名称', '基金类型']
        rows = [[f.id, f.fund_code, f.fund_name[:30] if f.fund_name else '', f.fund_type or ''] for f in funds]
        print_table('基金表 (Fund)', headers, rows)
    
    # 持仓表
    positions = UserPosition.query.all()
    if positions:
        headers = ['ID', '基金ID', '份额', '成本价', '购买日期']
        rows = [[p.id, p.fund_id, p.shares, p.cost_price, p.purchase_date or ''] for p in positions]
        print_table('持仓表 (UserPosition)', headers, rows)
    
    # 预警表
    alerts = FundAlert.query.all()
    if alerts:
        headers = ['ID', '基金ID', '预警类型', '阈值', '是否激活']
        rows = [[a.id, a.fund_id, a.alert_type, a.threshold, '是' if a.is_active else '否'] for a in alerts]
        print_table('预警表 (FundAlert)', headers, rows)
    else:
        print("\n预警表 (FundAlert): 无数据")
    
    # 净值表 (只显示最近5条)
    net_values = FundNetValue.query.order_by(FundNetValue.date.desc()).limit(5).all()
    if net_values:
        headers = ['ID', '基金ID', '日期', '单位净值', '累计净值', '日涨跌幅']
        rows = [[nv.id, nv.fund_id, nv.date, nv.unit_net_value, nv.accumulated_net_value, f"{nv.daily_growth_rate}%" if nv.daily_growth_rate else ''] for nv in net_values]
        print_table('净值表 (FundNetValue) - 最近5条', headers, rows)
    else:
        print("\n净值表 (FundNetValue): 无数据")
    
    # 统计信息
    print("\n" + "="*80)
    print(" 统计信息")
    print("="*80)
    print(f"  基金数量: {Fund.query.count()}")
    print(f"  持仓数量: {UserPosition.query.count()}")
    print(f"  预警数量: {FundAlert.query.count()}")
    print(f"  净值记录: {FundNetValue.query.count()}")
    
    # 持仓汇总
    if positions:
        total_market_value = 0
        total_cost_value = 0
        
        print("\n" + "="*80)
        print(" 持仓汇总")
        print("="*80)
        
        for pos in positions:
            fund = db.session.get(Fund, pos.fund_id)
            cost_value = pos.shares * pos.cost_price
            total_cost_value += cost_value
            
            print(f"  {fund.fund_code} - {fund.fund_name}")
            print(f"    份额: {pos.shares} | 成本价: {pos.cost_price} | 成本: ¥{cost_value:.2f}")
        
        print(f"\n  总成本: ¥{total_cost_value:.2f}")
