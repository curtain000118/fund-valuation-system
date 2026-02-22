"""
主页面路由
"""
from flask import Blueprint, render_template, jsonify
from app import db
from models import Fund, UserPosition, FundAlert
from services.data_fetcher import FundDataFetcher
from services.valuation_engine import ValuationEngine

main = Blueprint('main', __name__)
fetcher = FundDataFetcher()
engine = ValuationEngine()

@main.route('/')
def index():
    """首页"""
    return render_template('index.html')

@main.route('/portfolio')
def portfolio():
    """持仓管理页面"""
    return render_template('portfolio.html')

@main.route('/alerts')
def alerts():
    """预警管理页面"""
    return render_template('alerts.html')

@main.route('/analysis')
def analysis():
    """数据分析页面"""
    return render_template('analysis.html')

@main.route('/fund/<fund_code>')
def fund_detail(fund_code):
    """基金详情页面"""
    return render_template('fund_detail.html', fund_code=fund_code)
