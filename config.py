"""
基金实时估值系统配置文件
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fund-valuation-secret-key-2024'
    
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
    
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///fund_system.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    
    TUSHARE_TOKEN = os.environ.get('TUSHARE_TOKEN', '')
    
    UPDATE_INTERVAL = 60
    
    ALERT_THRESHOLD_UP = 5.0
    ALERT_THRESHOLD_DOWN = -5.0
    
    FUNDAPI_BASE_URL = 'https://fund.eastmoney.com'
    
    VERCEL_ENV = os.environ.get('VERCEL_ENV', 'development')
    IS_VERCEL = VERCEL_ENV in ['production', 'preview']

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class VercelConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'vercel': VercelConfig,
    'default': DevelopmentConfig
}
