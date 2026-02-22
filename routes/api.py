"""
API路由
"""
from flask import Blueprint, jsonify, request
from app import db
from models import Fund, FundNetValue, UserPosition, FundAlert
from services.data_fetcher import FundDataFetcher
from services.valuation_engine import ValuationEngine
from datetime import datetime, date

api = Blueprint('api', __name__)
fetcher = FundDataFetcher()
engine = ValuationEngine()

@api.route('/funds/search', methods=['GET'])
def search_funds():
    """搜索基金"""
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return jsonify({'error': '请提供搜索关键词'}), 400
    
    funds = fetcher.search_fund(keyword)
    return jsonify({'funds': funds})

@api.route('/funds/<fund_code>', methods=['GET'])
def get_fund_info(fund_code):
    """获取基金信息"""
    fund_info = fetcher.get_fund_info(fund_code)
    
    if not fund_info:
        return jsonify({'error': '未找到该基金'}), 404
    
    return jsonify(fund_info)

@api.route('/funds/<fund_code>/detail', methods=['GET'])
def get_fund_detail(fund_code):
    """获取基金详细信息"""
    detail = fetcher.get_fund_detail(fund_code)
    
    if not detail:
        return jsonify({'error': '未找到该基金详细信息'}), 404
    
    return jsonify(detail)

@api.route('/funds/<fund_code>/net-values', methods=['GET'])
def get_fund_net_values(fund_code):
    """获取基金历史净值"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 30, type=int)
    
    net_values = fetcher.get_fund_net_values(fund_code, page, size)
    return jsonify({'net_values': net_values})

@api.route('/funds/<fund_code>/valuation', methods=['GET'])
def get_realtime_valuation(fund_code):
    """获取基金实时估值"""
    valuation = engine.get_realtime_valuation(fund_code)
    
    if not valuation:
        valuation = {
            'fund_code': fund_code,
            'fund_name': None,
            'unit_net_value': None,
            'estimated_value': None,
            'estimated_growth_rate': None,
            'update_time': None
        }
    
    return jsonify(valuation)

@api.route('/funds/<fund_code>/intraday', methods=['GET'])
def get_fund_intraday(fund_code):
    """获取基金分时数据"""
    intraday = fetcher.get_fund_intraday_data(fund_code)
    
    if not intraday:
        return jsonify({'error': '无法获取分时数据'}), 404
    
    return jsonify(intraday)

@api.route('/funds/rank', methods=['GET'])
def get_fund_rank():
    """获取基金排行"""
    fund_type = request.args.get('type', 'all')
    sort_field = request.args.get('sort', 'zzf')
    sort_order = request.args.get('order', 'desc')
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 50, type=int)
    
    funds = fetcher.get_fund_rank(fund_type, sort_field, sort_order, page, size)
    return jsonify({'funds': funds})

@api.route('/positions', methods=['GET'])
def get_positions():
    """获取所有持仓"""
    positions = UserPosition.query.all()
    
    portfolio_value = engine.calculate_portfolio_value(positions)
    return jsonify(portfolio_value)

@api.route('/positions', methods=['POST'])
def add_position():
    """添加持仓"""
    data = request.get_json()
    
    fund_code = data.get('fund_code')
    shares = data.get('shares')
    cost_price = data.get('cost_price')
    market_value = data.get('market_value')
    profit = data.get('profit')
    dividend_type = data.get('dividend_type', 'cash')
    purchase_date = data.get('purchase_date')
    
    if not all([fund_code, shares, cost_price]):
        return jsonify({'error': '缺少必要参数'}), 400
    
    fund = Fund.query.filter_by(fund_code=fund_code).first()
    
    if not fund:
        fund_info = fetcher.get_fund_info(fund_code)
        
        if not fund_info:
            return jsonify({'error': '未找到该基金，请确认基金代码是否正确'}), 404
        
        fund = Fund(
            fund_code=fund_code,
            fund_name=fund_info.get('fund_name', ''),
            fund_type=fund_info.get('fund_type', '')
        )
        db.session.add(fund)
        db.session.commit()
    
    position = UserPosition(
        fund_id=fund.id,
        shares=float(shares),
        cost_price=float(cost_price),
        market_value=float(market_value) if market_value else None,
        profit=float(profit) if profit else None,
        dividend_type=dividend_type,
        purchase_date=datetime.strptime(purchase_date, '%Y-%m-%d').date() if purchase_date else None
    )
    
    db.session.add(position)
    db.session.commit()
    
    return jsonify({'message': '持仓添加成功', 'position': position.to_dict()}), 201

@api.route('/positions/<int:position_id>', methods=['PUT'])
def update_position(position_id):
    """更新持仓"""
    position = UserPosition.query.get_or_404(position_id)
    data = request.get_json()
    
    if 'shares' in data:
        position.shares = float(data['shares'])
    if 'cost_price' in data:
        position.cost_price = float(data['cost_price'])
    if 'market_value' in data:
        position.market_value = float(data['market_value']) if data['market_value'] else None
    if 'profit' in data:
        position.profit = float(data['profit']) if data['profit'] else None
    if 'dividend_type' in data:
        position.dividend_type = data['dividend_type']
    if 'purchase_date' in data:
        position.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify({'message': '持仓更新成功', 'position': position.to_dict()})

@api.route('/positions/<int:position_id>', methods=['DELETE'])
def delete_position(position_id):
    """删除持仓"""
    position = UserPosition.query.get_or_404(position_id)
    
    db.session.delete(position)
    db.session.commit()
    
    return jsonify({'message': '持仓删除成功'})

@api.route('/alerts', methods=['GET'])
def get_alerts():
    """获取所有预警"""
    alerts = FundAlert.query.filter_by(is_active=True).all()
    return jsonify({'alerts': [alert.to_dict() for alert in alerts]})

@api.route('/alerts', methods=['POST'])
def add_alert():
    """添加预警"""
    data = request.get_json()
    
    fund_code = data.get('fund_code')
    alert_type = data.get('alert_type')
    threshold = data.get('threshold')
    
    if not all([fund_code, alert_type, threshold]):
        return jsonify({'error': '缺少必要参数'}), 400
    
    fund = Fund.query.filter_by(fund_code=fund_code).first()
    
    if not fund:
        fund_info = fetcher.get_fund_info(fund_code)
        
        if not fund_info:
            return jsonify({'error': '未找到该基金'}), 404
        
        fund = Fund(
            fund_code=fund_code,
            fund_name=fund_info.get('fund_name', ''),
            fund_type=fund_info.get('fund_type', '')
        )
        db.session.add(fund)
        db.session.commit()
    
    alert = FundAlert(
        fund_id=fund.id,
        alert_type=alert_type,
        threshold=float(threshold)
    )
    
    db.session.add(alert)
    db.session.commit()
    
    return jsonify({'message': '预警添加成功', 'alert': alert.to_dict()}), 201

@api.route('/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """删除预警"""
    alert = FundAlert.query.get_or_404(alert_id)
    
    db.session.delete(alert)
    db.session.commit()
    
    return jsonify({'message': '预警删除成功'})

@api.route('/portfolio/summary', methods=['GET'])
def get_portfolio_summary():
    """获取投资组合摘要"""
    positions = UserPosition.query.all()
    
    if not positions:
        return jsonify({
            'total_market_value': 0,
            'total_cost_value': 0,
            'total_profit': 0,
            'total_profit_rate': 0,
            'positions': []
        })
    
    portfolio_value = engine.calculate_portfolio_value(positions)
    return jsonify(portfolio_value)
