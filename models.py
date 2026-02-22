"""
数据模型定义
"""
from datetime import datetime
from app import db

class Fund(db.Model):
    __tablename__ = 'funds'
    
    id = db.Column(db.Integer, primary_key=True)
    fund_code = db.Column(db.String(10), unique=True, nullable=False)
    fund_name = db.Column(db.String(100), nullable=False)
    fund_type = db.Column(db.String(20))
    manager = db.Column(db.String(50))
    company = db.Column(db.String(100))
    establish_date = db.Column(db.Date)
    scale = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    net_values = db.relationship('FundNetValue', backref='fund', lazy='dynamic', 
                                  cascade='all, delete-orphan')
    positions = db.relationship('UserPosition', backref='fund', lazy='dynamic',
                                cascade='all, delete-orphan')
    alerts = db.relationship('FundAlert', backref='fund', lazy='dynamic',
                             cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'fund_code': self.fund_code,
            'fund_name': self.fund_name,
            'fund_type': self.fund_type,
            'manager': self.manager,
            'company': self.company,
            'scale': self.scale
        }

class FundNetValue(db.Model):
    __tablename__ = 'fund_net_values'
    
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    unit_net_value = db.Column(db.Float, nullable=False)
    accumulated_net_value = db.Column(db.Float)
    daily_growth_rate = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('fund_id', 'date'), )
    
    def to_dict(self):
        return {
            'id': self.id,
            'fund_id': self.fund_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'unit_net_value': self.unit_net_value,
            'accumulated_net_value': self.accumulated_net_value,
            'daily_growth_rate': self.daily_growth_rate
        }

class UserPosition(db.Model):
    __tablename__ = 'user_positions'
    
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    market_value = db.Column(db.Float)
    profit = db.Column(db.Float)
    dividend_type = db.Column(db.String(20), default='cash')
    purchase_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'fund_id': self.fund_id,
            'fund_code': self.fund.fund_code,
            'fund_name': self.fund.fund_name,
            'shares': self.shares,
            'cost_price': self.cost_price,
            'market_value': self.market_value,
            'profit': self.profit,
            'dividend_type': self.dividend_type or 'cash',
            'purchase_date': self.purchase_date.strftime('%Y-%m-%d') if self.purchase_date else None
        }

class FundAlert(db.Model):
    __tablename__ = 'fund_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('funds.id'), nullable=False)
    alert_type = db.Column(db.String(20), nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    triggered_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'fund_id': self.fund_id,
            'fund_code': self.fund.fund_code,
            'fund_name': self.fund.fund_name,
            'alert_type': self.alert_type,
            'threshold': self.threshold,
            'is_active': self.is_active,
            'triggered_at': self.triggered_at.strftime('%Y-%m-%d %H:%M:%S') if self.triggered_at else None
        }
