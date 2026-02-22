"""
Vercel Cron Job - 定时更新基金数据
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import jsonify, request
from app import create_app, db
from models import Fund, FundNetValue
from services.data_fetcher import DataFetcher

app = create_app()

def verify_auth():
    """
    验证授权
    """
    auth_header = request.headers.get('Authorization', '')
    cron_secret = os.environ.get('CRON_SECRET', '')
    
    if cron_secret:
        if not auth_header.startswith('Bearer '):
            return False
        token = auth_header.replace('Bearer ', '')
        return token == cron_secret
    
    return True

def update_funds():
    """
    定时任务：更新基金净值数据
    """
    with app.app_context():
        try:
            fetcher = DataFetcher()
            funds = Fund.query.all()
            
            updated_count = 0
            failed_count = 0
            
            for fund in funds:
                try:
                    data = fetcher.get_fund_realtime_estimate(fund.fund_code)
                    if data:
                        net_value = FundNetValue(
                            fund_code=fund.fund_code,
                            date=datetime.now().date(),
                            net_value=data.get('net_value'),
                            accumulated_value=data.get('accumulated_value'),
                            daily_growth=data.get('daily_growth_rate')
                        )
                        db.session.add(net_value)
                        updated_count += 1
                except Exception as e:
                    app.logger.error(f"更新基金 {fund.fund_code} 失败: {str(e)}")
                    failed_count += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'updated': updated_count,
                'failed': failed_count,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            app.logger.error(f"定时任务执行失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

def handler(request, response):
    """
    Vercel Serverless Function 处理器
    """
    if not verify_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        result = update_funds()
        return jsonify(result)
    else:
        return jsonify({'error': 'Method not allowed'}), 405
