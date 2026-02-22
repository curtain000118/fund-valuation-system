"""
基金估值计算引擎
"""
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
from models import Fund, FundNetValue, UserPosition
from services.data_fetcher import FundDataFetcher

class ValuationEngine:
    """基金估值计算引擎"""
    
    def __init__(self):
        self.fetcher = FundDataFetcher()
    
    def calculate_position_value(self, position: UserPosition, current_net_value: float, 
                                  prev_net_value: float = None, estimated_growth_rate: float = None) -> Dict:
        """
        计算持仓市值和收益
        :param position: 持仓对象
        :param current_net_value: 当前净值
        :param prev_net_value: 前一日净值
        :param estimated_growth_rate: 估算涨跌幅
        :return: 持仓价值字典
        """
        cost_value = position.shares * position.cost_price
        
        if position.market_value is not None and position.profit is not None:
            base_market_value = position.market_value
            base_profit = position.profit
        else:
            base_market_value = cost_value
            base_profit = 0
        
        today_profit = None
        current_market_value = base_market_value
        
        if estimated_growth_rate is not None:
            today_profit = base_market_value * estimated_growth_rate / 100
            current_market_value = base_market_value + today_profit
        elif prev_net_value and current_net_value:
            growth_rate = (current_net_value - prev_net_value) / prev_net_value * 100 if prev_net_value > 0 else 0
            today_profit = base_market_value * growth_rate / 100
            current_market_value = base_market_value + today_profit
        
        profit_rate = (base_profit / (base_market_value - base_profit) * 100) if (base_market_value - base_profit) > 0 else 0
        
        return {
            'position_id': position.id,
            'fund_code': position.fund.fund_code,
            'fund_name': position.fund.fund_name,
            'shares': position.shares,
            'cost_price': position.cost_price,
            'purchase_date': position.purchase_date.strftime('%Y-%m-%d') if position.purchase_date else None,
            'dividend_type': position.dividend_type or 'cash',
            'current_net_value': current_net_value,
            'market_value': round(current_market_value, 2),
            'base_market_value': round(base_market_value, 2),
            'cost_value': round(cost_value, 2),
            'profit': round(base_profit, 2),
            'profit_rate': round(profit_rate, 2),
            'today_profit': round(today_profit, 2) if today_profit is not None else None
        }
    
    def calculate_portfolio_value(self, positions: List[UserPosition]) -> Dict:
        """
        计算投资组合总价值
        :param positions: 持仓列表
        :return: 组合价值字典
        """
        total_market_value = 0
        total_cost_value = 0
        total_today_profit = 0
        total_profit = 0
        position_details = []
        
        for position in positions:
            fund_code = position.fund.fund_code
            fund_info = self.fetcher.get_fund_info(fund_code)
            
            latest_net_value = None
            prev_net_value = None
            estimated_growth_rate = None
            
            if fund_info:
                estimated_value = fund_info.get('estimated_value')
                unit_net_value = fund_info.get('unit_net_value')
                estimated_growth_rate = fund_info.get('estimated_growth_rate')
                
                if estimated_value:
                    latest_net_value = estimated_value
                    prev_net_value = unit_net_value
                else:
                    latest_net_value = unit_net_value
            
            if latest_net_value is None:
                latest_net_value = position.cost_price
            
            position_value = self.calculate_position_value(
                position, latest_net_value, prev_net_value, estimated_growth_rate
            )
            position_details.append(position_value)
            
            total_market_value += position_value['market_value']
            total_cost_value += position_value['cost_value']
            total_profit += position_value['profit']
            if position_value['today_profit'] is not None:
                total_today_profit += position_value['today_profit']
        
        total_profit_rate = (total_profit / (total_market_value - total_today_profit - total_profit) * 100) if (total_market_value - total_today_profit - total_profit) > 0 else 0
        
        return {
            'total_market_value': round(total_market_value, 2),
            'total_cost_value': round(total_cost_value, 2),
            'total_profit': round(total_profit, 2),
            'total_profit_rate': round(total_profit_rate, 2),
            'total_today_profit': round(total_today_profit, 2),
            'positions': position_details
        }
    
    def get_latest_net_value(self, fund_code: str) -> Optional[float]:
        """
        获取最新净值（优先使用估值）
        :param fund_code: 基金代码
        :return: 最新净值或估值
        """
        fund_info = self.fetcher.get_fund_info(fund_code)
        
        if fund_info:
            estimated_value = fund_info.get('estimated_value')
            if estimated_value:
                return estimated_value
            return fund_info.get('unit_net_value')
        return None
    
    def get_realtime_valuation(self, fund_code: str) -> Optional[Dict]:
        """
        获取实时估值
        :param fund_code: 基金代码
        :return: 实时估值数据
        """
        valuation = self.fetcher.get_realtime_valuation(fund_code)
        
        if valuation:
            unit_net_value = valuation.get('unit_net_value')
            
            if unit_net_value is None:
                net_values = self.fetcher.get_fund_net_values(fund_code, 1, 1)
                if net_values:
                    unit_net_value = net_values[0].get('unit_net_value')
            
            return {
                'fund_code': valuation.get('fund_code'),
                'fund_name': valuation.get('fund_name'),
                'unit_net_value': unit_net_value,
                'estimated_value': valuation.get('estimated_value'),
                'estimated_growth_rate': valuation.get('estimated_growth_rate'),
                'estimated_time': valuation.get('estimated_time'),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        return None
    
    def calculate_historical_return(self, net_values: List[FundNetValue], days: int = 30) -> Dict:
        """
        计算历史收益率
        :param net_values: 净值数据列表
        :param days: 计算天数
        :return: 收益率数据
        """
        if not net_values or len(net_values) < 2:
            return {
                'return_rate': 0,
                'annualized_return': 0,
                'max_drawdown': 0,
                'volatility': 0
            }
        
        sorted_values = sorted(net_values, key=lambda x: x.date, reverse=True)[:days]
        
        if len(sorted_values) < 2:
            return {
                'return_rate': 0,
                'annualized_return': 0,
                'max_drawdown': 0,
                'volatility': 0
            }
        
        latest_value = sorted_values[0].unit_net_value
        earliest_value = sorted_values[-1].unit_net_value
        return_rate = (latest_value - earliest_value) / earliest_value * 100
        
        annualized_return = return_rate * (365 / days) if days > 0 else 0
        
        values = [v.unit_net_value for v in sorted_values]
        peak = values[0]
        max_drawdown = 0
        
        for value in values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        daily_returns = []
        for i in range(len(values) - 1):
            daily_return = (values[i] - values[i + 1]) / values[i + 1]
            daily_returns.append(daily_return)
        
        volatility = 0
        if daily_returns:
            mean_return = sum(daily_returns) / len(daily_returns)
            variance = sum((r - mean_return) ** 2 for r in daily_returns) / len(daily_returns)
            volatility = (variance ** 0.5) * (252 ** 0.5) * 100
        
        return {
            'return_rate': round(return_rate, 2),
            'annualized_return': round(annualized_return, 2),
            'max_drawdown': round(max_drawdown, 2),
            'volatility': round(volatility, 2)
        }
    
    def estimate_today_profit(self, position: UserPosition, estimated_growth_rate: float) -> Dict:
        """
        估算今日收益
        :param position: 持仓对象
        :param estimated_growth_rate: 估算涨跌幅
        :return: 估算收益数据
        """
        latest_net_value = self.get_latest_net_value(position.fund.fund_code)
        
        if latest_net_value:
            estimated_value = latest_net_value * (1 + estimated_growth_rate / 100)
            estimated_profit = position.shares * (estimated_value - latest_net_value)
            
            return {
                'fund_code': position.fund.fund_code,
                'fund_name': position.fund.fund_name,
                'shares': position.shares,
                'latest_net_value': latest_net_value,
                'estimated_value': round(estimated_value, 4),
                'estimated_growth_rate': estimated_growth_rate,
                'estimated_profit': round(estimated_profit, 2)
            }
        return None
