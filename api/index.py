"""
Vercel Serverless Function 入口文件
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models import Fund, FundNetValue, UserPosition, FundAlert

app = create_app()

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.error(f"数据库初始化失败: {str(e)}")

def handler(request, response):
    """
    Vercel Serverless Function 处理器
    """
    return app(request, response)
