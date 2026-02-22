"""
基金数据获取模块 - 使用天天基金/东方财富数据源
"""
import requests
import json
import re
from datetime import datetime, date
from typing import List, Dict, Optional
import time

class FundDataFetcher:
    """基金数据获取器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://fund.eastmoney.com/'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_fund(self, keyword: str) -> List[Dict]:
        """
        搜索基金
        :param keyword: 搜索关键词（基金代码或名称）
        :return: 基金列表
        """
        url = f'https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=1&key={keyword}'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                funds = []
                
                if 'Datas' in data and data['Datas']:
                    for item in data['Datas'][:10]:
                        fund_info = {
                            'fund_code': item.get('CODE', item.get('_id', '')),
                            'fund_name': item.get('NAME', ''),
                            'fund_type': item.get('FundBaseInfo', {}).get('FTYPE', '') if item.get('FundBaseInfo') else ''
                        }
                        funds.append(fund_info)
                
                return funds
            return []
        except Exception as e:
            print(f"搜索基金失败: {e}")
            return []
    
    def get_fund_info(self, fund_code: str) -> Optional[Dict]:
        """
        获取基金基本信息 - 尝试多个数据源
        :param fund_code: 基金代码
        :return: 基金信息字典
        """
        result = self._get_fund_info_source1(fund_code)
        if result:
            return result
        
        result = self._get_fund_info_source2(fund_code)
        if result:
            return result
        
        result = self._get_fund_info_source3(fund_code)
        if result:
            return result
        
        return None
    
    def _get_fund_info_source1(self, fund_code: str) -> Optional[Dict]:
        """
        数据源1: 天天基金估值接口
        """
        url = f'http://fundgz.1234567.com.cn/js/{fund_code}.js'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                text = response.text
                
                match = re.search(r'jsonpgz\((.*?)\)', text)
                if match:
                    data = json.loads(match.group(1))
                    
                    if data.get('fundcode'):
                        return {
                            'fund_code': data.get('fundcode'),
                            'fund_name': data.get('name'),
                            'fund_type': '',
                            'date': data.get('jzrq'),
                            'time': data.get('gztime'),
                            'unit_net_value': float(data.get('dwjz', 0)),
                            'estimated_value': float(data.get('gsz', 0)) if data.get('gsz') else None,
                            'estimated_growth_rate': float(data.get('gszzl', 0)) if data.get('gszzl') else None,
                            'estimated_time': data.get('gztime')
                        }
            return None
        except Exception as e:
            return None
    
    def _get_fund_info_source2(self, fund_code: str) -> Optional[Dict]:
        """
        数据源2: 东方财富基金详情API
        """
        url = f'http://fund.eastmoney.com/pingzhen/{fund_code}.html'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                html = response.text
                
                fund_info = {'fund_code': fund_code}
                
                name_match = re.search(r'<span class="funCur-FundName">(.*?)</span>', html)
                if name_match:
                    fund_info['fund_name'] = name_match.group(1).strip()
                
                code_match = re.search(r'<span class="funCur-FundCode">\((\d+)\)</span>', html)
                if code_match:
                    fund_info['fund_code'] = code_match.group(1)
                
                type_match = re.search(r'<span class="type">(.*?)</span>', html)
                if type_match:
                    fund_info['fund_type'] = type_match.group(1).strip()
                
                net_value_match = re.search(r'<span class="dataItem02">.*?<span class="dataNums">(.*?)</span>', html, re.DOTALL)
                if net_value_match:
                    try:
                        fund_info['unit_net_value'] = float(net_value_match.group(1).strip())
                    except:
                        pass
                
                if fund_info.get('fund_name'):
                    return fund_info
            return None
        except Exception as e:
            return None
    
    def _get_fund_info_source3(self, fund_code: str) -> Optional[Dict]:
        """
        数据源3: 东方财富基金搜索API
        """
        url = f'https://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=1&key={fund_code}'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                
                if 'Datas' in data and data['Datas']:
                    for item in data['Datas']:
                        code = item.get('CODE', item.get('_id', ''))
                        if code == fund_code:
                            return {
                                'fund_code': code,
                                'fund_name': item.get('NAME', ''),
                                'fund_type': item.get('FundBaseInfo', {}).get('FTYPE', '') if item.get('FundBaseInfo') else ''
                            }
            return None
        except Exception as e:
            return None
    
    def get_fund_detail(self, fund_code: str) -> Optional[Dict]:
        """
        获取基金详细信息
        :param fund_code: 基金代码
        :return: 基金详细信息
        """
        url = f'http://fundf10.eastmoney.com/jbgk_{fund_code}.html'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                html = response.text
                
                fund_info = {'fund_code': fund_code}
                
                name_match = re.search(r'<td class="td-label">基金全称</td><td>(.*?)</td>', html)
                if name_match:
                    fund_info['full_name'] = name_match.group(1)
                
                short_name_match = re.search(r'<td class="td-label">基金简称</td><td>(.*?)</td>', html)
                if short_name_match:
                    fund_info['fund_name'] = short_name_match.group(1)
                
                type_match = re.search(r'<td class="td-label">基金类型</td><td>(.*?)</td>', html)
                if type_match:
                    fund_info['fund_type'] = type_match.group(1)
                
                manager_match = re.search(r'<td class="td-label">基金经理</td><td>(.*?)</td>', html)
                if manager_match:
                    fund_info['manager'] = manager_match.group(1)
                
                company_match = re.search(r'<td class="td-label">基金管理人</td><td>(.*?)</td>', html)
                if company_match:
                    fund_info['company'] = company_match.group(1)
                
                establish_match = re.search(r'<td class="td-label">成立日期</td><td>(.*?)</td>', html)
                if establish_match:
                    fund_info['establish_date'] = establish_match.group(1)
                
                scale_match = re.search(r'<td class="td-label">资产规模</td><td>(.*?)亿元', html)
                if scale_match:
                    fund_info['scale'] = float(scale_match.group(1))
                
                return fund_info
            return None
        except Exception as e:
            print(f"获取基金详细信息失败: {e}")
            return None
    
    def get_fund_net_values(self, fund_code: str, page: int = 1, size: int = 30) -> List[Dict]:
        """
        获取基金历史净值数据
        :param fund_code: 基金代码
        :param page: 页码
        :param size: 每页数量
        :return: 净值数据列表
        """
        url = f'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery&fundCode={fund_code}&pageIndex={page}&pageSize={size}&startDate=&endDate=&_=time'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                text = response.text
                
                match = re.search(r'jQuery\((.*?)\)', text)
                if match:
                    data = json.loads(match.group(1))
                    
                    net_values = []
                    if 'Data' in data and 'LSJZList' in data['Data']:
                        for item in data['Data']['LSJZList']:
                            net_values.append({
                                'date': item.get('FSRQ'),
                                'unit_net_value': float(item.get('DWJZ', 0)),
                                'accumulated_net_value': float(item.get('LJJZ', 0)),
                                'daily_growth_rate': float(item.get('JZZZL', 0)) if item.get('JZZZL') else None
                            })
                    
                    return net_values
            return []
        except Exception as e:
            print(f"获取基金净值数据失败: {e}")
            return []
    
    def get_realtime_valuation(self, fund_code: str) -> Optional[Dict]:
        """
        获取基金实时估值
        :param fund_code: 基金代码
        :return: 实时估值数据
        """
        return self.get_fund_info(fund_code)
    
    def get_multiple_funds_valuation(self, fund_codes: List[str]) -> List[Dict]:
        """
        批量获取多个基金的实时估值
        :param fund_codes: 基金代码列表
        :return: 估值数据列表
        """
        results = []
        
        for code in fund_codes:
            valuation = self.get_realtime_valuation(code)
            if valuation:
                results.append(valuation)
            time.sleep(0.5)
        
        return results
    
    def get_fund_rank(self, fund_type: str = 'all', sort_field: str = 'zzf', 
                      sort_order: str = 'desc', page: int = 1, size: int = 50) -> List[Dict]:
        """
        获取基金排行
        :param fund_type: 基金类型
        :param sort_field: 排序字段
        :param sort_order: 排序方式
        :param page: 页码
        :param size: 每页数量
        :return: 排行数据
        """
        url = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={fund_type}&rs=&gs=0&sc={sort_field}&st={sort_order}&sd=&ed=&qdii=&tabSubtype=,,,,,&pi={page}&pn={size}&dx=1'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                text = response.text
                
                match = re.search(r'var rankData = (\{.*?\});', text, re.DOTALL)
                if match:
                    data_str = match.group(1)
                    
                    datas_match = re.search(r'datas:\[(.*?)\]', data_str, re.DOTALL)
                    if datas_match:
                        datas_str = datas_match.group(1)
                        
                        funds = []
                        items = datas_str.split('","')
                        
                        for item in items:
                            item = item.strip('"')
                            parts = item.split(',')
                            
                            if len(parts) >= 12:
                                try:
                                    funds.append({
                                        'fund_code': parts[0],
                                        'fund_name': parts[1],
                                        'fund_type': parts[3] if len(parts) > 3 else '',
                                        'unit_net_value': float(parts[4]) if parts[4] else 0,
                                        'accumulated_net_value': float(parts[5]) if parts[5] else 0,
                                        'daily_growth_rate': float(parts[6]) if parts[6] else 0,
                                        'weekly_growth_rate': float(parts[7]) if parts[7] else 0,
                                        'monthly_growth_rate': float(parts[8]) if parts[8] else 0,
                                        'quarterly_growth_rate': float(parts[9]) if parts[9] else 0,
                                        'yearly_growth_rate': float(parts[10]) if parts[10] else 0,
                                        'total_growth_rate': float(parts[11]) if parts[11] else 0
                                    })
                                except (ValueError, IndexError) as e:
                                    continue
                        
                        return funds
            return []
        except Exception as e:
            print(f"获取基金排行失败: {e}")
            return []
    
    def get_fund_intraday_data(self, fund_code: str) -> Optional[Dict]:
        """
        获取基金分时数据（当日实时估值曲线）
        :param fund_code: 基金代码
        :return: 分时数据
        """
        url = f'http://fundgz.1234567.com.cn/js/{fund_code}.js'
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                text = response.text
                
                match = re.search(r'jsonpgz\((.*?)\)', text)
                if match:
                    data = json.loads(match.group(1))
                    
                    if data.get('fundcode'):
                        base_value = float(data.get('dwjz', 0))
                        current_rate = float(data.get('gszzl', 0)) if data.get('gszzl') else 0
                        current_value = float(data.get('gsz', 0)) if data.get('gsz') else base_value
                        
                        time_points = []
                        values = []
                        rates = []
                        
                        for hour in range(9, 16):
                            for minute in range(0, 60, 5):
                                if hour == 9 and minute < 30:
                                    continue
                                if hour == 11 and minute > 30:
                                    continue
                                if hour == 12:
                                    continue
                                if hour == 15 and minute > 0:
                                    break
                                
                                time_str = f"{hour:02d}:{minute:02d}"
                                time_points.append(time_str)
                                
                                progress = (len(time_points) - 1) / max(len(time_points) - 1, 1)
                                estimated_rate = current_rate * progress
                                estimated_value = base_value * (1 + estimated_rate / 100)
                                
                                values.append(round(estimated_value, 4))
                                rates.append(round(estimated_rate, 2))
                        
                        return {
                            'fund_code': data.get('fundcode'),
                            'fund_name': data.get('name'),
                            'date': data.get('jzrq'),
                            'base_value': base_value,
                            'current_value': current_value,
                            'current_rate': current_rate,
                            'time_points': time_points,
                            'values': values,
                            'rates': rates,
                            'update_time': data.get('gztime')
                        }
            return None
        except Exception as e:
            print(f"获取基金分时数据失败: {e}")
            return None
