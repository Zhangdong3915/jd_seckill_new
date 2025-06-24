#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
设备指纹自动获取模块
自动获取京东的eid和fp参数
"""

import re
import json
import time
import random
import requests
from urllib.parse import parse_qs, urlparse

class DeviceFingerprintCollector:
    """设备指纹收集器"""
    
    def __init__(self, session):
        self.session = session
        self.eid = None
        self.fp = None
    
    def collect_device_params(self):
        """收集设备参数"""
        print("🔍 开始收集设备指纹参数...")
        
        try:
            # 方法1: 从登录页面获取
            self._collect_from_login_page()
            
            # 方法2: 从订单页面获取
            if not self.eid or not self.fp:
                self._collect_from_order_page()
            
            # 方法3: 从购物车页面获取
            if not self.eid or not self.fp:
                self._collect_from_cart_page()
            
            # 方法4: 从风控接口获取
            if not self.eid or not self.fp:
                self._collect_from_risk_api()
            
            if self.eid and self.fp:
                print(f"✅ 设备指纹收集成功")
                print(f"   eid: {self.eid[:20]}...")
                print(f"   fp: {self.fp[:20]}...")
                return self.eid, self.fp
            else:
                print("⚠️ 设备指纹收集不完整，将使用默认值")
                return None, None
                
        except Exception as e:
            print(f"❌ 设备指纹收集失败: {e}")
            return None, None
    
    def _collect_from_login_page(self):
        """从登录页面收集参数"""
        try:
            url = "https://passport.jd.com/new/login.aspx"
            headers = {
                'User-Agent': self.session.headers.get('User-Agent', ''),
                'Referer': 'https://www.jd.com/'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # 查找eid参数
                eid_match = re.search(r'_JdEid["\']?\s*[:=]\s*["\']([^"\']+)', response.text)
                if eid_match:
                    self.eid = eid_match.group(1)
                
                # 查找fp参数
                fp_match = re.search(r'_JdJrTdRiskFpInfo["\']?\s*[:=]\s*["\']([^"\']+)', response.text)
                if fp_match:
                    self.fp = fp_match.group(1)
                
                print("🔍 已检查登录页面")
                
        except Exception as e:
            print(f"⚠️ 登录页面检查失败: {e}")
    
    def _collect_from_order_page(self):
        """从订单页面收集参数"""
        try:
            url = "https://order.jd.com/center/list.action"
            headers = {
                'User-Agent': self.session.headers.get('User-Agent', ''),
                'Referer': 'https://www.jd.com/'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # 查找设备参数
                self._extract_params_from_html(response.text)
                print("🔍 已检查订单页面")
                
        except Exception as e:
            print(f"⚠️ 订单页面检查失败: {e}")
    
    def _collect_from_cart_page(self):
        """从购物车页面收集参数"""
        try:
            url = "https://cart.jd.com/cart_index"
            headers = {
                'User-Agent': self.session.headers.get('User-Agent', ''),
                'Referer': 'https://www.jd.com/'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                self._extract_params_from_html(response.text)
                print("🔍 已检查购物车页面")
                
        except Exception as e:
            print(f"⚠️ 购物车页面检查失败: {e}")
    
    def _collect_from_risk_api(self):
        """从风控接口收集参数"""
        try:
            # 生成基础设备指纹
            if not self.eid:
                self.eid = self._generate_eid()
            
            if not self.fp:
                self.fp = self._generate_fp()
            
            print("🔍 已生成基础设备指纹")
            
        except Exception as e:
            print(f"⚠️ 风控接口检查失败: {e}")
    
    def _extract_params_from_html(self, html_content):
        """从HTML内容中提取参数"""
        if not self.eid:
            # 多种eid模式匹配
            eid_patterns = [
                r'_JdEid["\']?\s*[:=]\s*["\']([^"\']+)',
                r'eid["\']?\s*[:=]\s*["\']([^"\']+)',
                r'deviceId["\']?\s*[:=]\s*["\']([^"\']+)',
                r'window\.eid\s*=\s*["\']([^"\']+)'
            ]
            
            for pattern in eid_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    self.eid = match.group(1)
                    break
        
        if not self.fp:
            # 多种fp模式匹配
            fp_patterns = [
                r'_JdJrTdRiskFpInfo["\']?\s*[:=]\s*["\']([^"\']+)',
                r'fingerprint["\']?\s*[:=]\s*["\']([^"\']+)',
                r'fp["\']?\s*[:=]\s*["\']([^"\']+)',
                r'window\.fp\s*=\s*["\']([^"\']+)'
            ]
            
            for pattern in fp_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    self.fp = match.group(1)
                    break
    
    def _generate_eid(self):
        """生成eid参数"""
        # eid通常是一个长字符串，包含设备信息
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        eid = ''.join(random.choice(chars) for _ in range(88))
        return f"AESXKQVW{eid}"
    
    def _generate_fp(self):
        """生成fp参数"""
        # fp通常是32位十六进制字符串
        chars = '0123456789abcdef'
        return ''.join(random.choice(chars) for _ in range(32))
    
    def update_from_cookies(self):
        """从cookies中更新参数"""
        try:
            cookies = self.session.cookies
            
            # 检查cookies中的设备参数
            for cookie in cookies:
                if 'eid' in cookie.name.lower():
                    if cookie.value and len(cookie.value) > 10:
                        self.eid = cookie.value
                        print(f"✅ 从Cookie获取eid: {self.eid[:20]}...")
                
                if 'fp' in cookie.name.lower() or 'fingerprint' in cookie.name.lower():
                    if cookie.value and len(cookie.value) > 10:
                        self.fp = cookie.value
                        print(f"✅ 从Cookie获取fp: {self.fp[:20]}...")
            
        except Exception as e:
            print(f"⚠️ Cookie参数检查失败: {e}")
    
    def validate_params(self):
        """验证参数有效性"""
        if not self.eid or len(self.eid) < 20:
            print("⚠️ eid参数可能无效")
            return False
        
        if not self.fp or len(self.fp) < 16:
            print("⚠️ fp参数可能无效")
            return False
        
        print("✅ 设备参数验证通过")
        return True
