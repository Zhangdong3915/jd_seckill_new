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
            # 清空现有参数，强制重新收集
            self.eid = None
            self.fp = None

            # 方法1: 从登录页面获取
            self._collect_from_login_page()

            # 方法2: 从订单页面获取
            if not self.eid or not self.fp:
                self._collect_from_order_page()

            # 方法3: 从购物车页面获取
            if not self.eid or not self.fp:
                self._collect_from_cart_page()

            # 方法4: 从风控接口获取（生成新的设备指纹）
            if not self.eid or not self.fp:
                self._collect_from_risk_api()

            if self.eid and self.fp:
                print(f"✅ 设备指纹收集成功")
                print(f"   eid: {self.eid[:20]}...")
                print(f"   fp: {self.fp[:20]}...")
                return self.eid, self.fp
            else:
                print("⚠️ 设备指纹收集不完整，生成新的设备指纹")
                # 强制生成新的设备指纹
                self.eid = self._generate_eid()
                self.fp = self._generate_fp()
                print(f"✅ 生成新的设备指纹")
                print(f"   eid: {self.eid[:20]}...")
                print(f"   fp: {self.fp[:20]}...")
                return self.eid, self.fp

        except Exception as e:
            print(f"❌ 设备指纹收集失败: {e}")
            # 即使出错也生成新的设备指纹
            try:
                self.eid = self._generate_eid()
                self.fp = self._generate_fp()
                print(f"✅ 生成备用设备指纹")
                print(f"   eid: {self.eid[:20]}...")
                print(f"   fp: {self.fp[:20]}...")
                return self.eid, self.fp
            except Exception as e2:
                print(f"❌ 生成备用设备指纹也失败: {e2}")
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
            # 先尝试从订单列表页面获取
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

            # 如果还没有获取到参数，尝试访问结算页面
            if not self.eid or not self.fp:
                self._collect_from_checkout_page()

        except Exception as e:
            print(f"⚠️ 订单页面检查失败: {e}")

    def _collect_from_checkout_page(self):
        """从结算页面收集真实的设备指纹参数"""
        try:
            print("🔍 尝试从结算页面获取真实设备指纹...")

            # 方法1: 尝试访问购物车结算页面
            cart_url = "https://cart.jd.com/cart_index"
            headers = {
                'User-Agent': self.session.headers.get('User-Agent', ''),
                'Referer': 'https://www.jd.com/'
            }

            response = self.session.get(cart_url, headers=headers, timeout=10)
            if response.status_code == 200:
                # 查找JavaScript中的设备指纹变量
                self._extract_js_variables(response.text)

            # 方法2: 如果购物车页面没有，尝试商品页面
            if not self.eid or not self.fp:
                # 使用茅台商品页面
                from maotai.config import global_config
                sku_id = global_config.getRaw('config', 'sku_id')
                product_url = f"https://item.jd.com/{sku_id}.html"

                response = self.session.get(product_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    self._extract_js_variables(response.text)

        except Exception as e:
            print(f"⚠️ 结算页面检查失败: {e}")

    def _extract_js_variables(self, html_content):
        """从HTML中提取JavaScript变量中的设备指纹"""
        import re

        # 查找 _JdEid 变量
        if not self.eid:
            # 多种可能的_JdEid模式
            eid_patterns = [
                r'_JdEid\s*=\s*["\']([^"\']+)["\']',
                r'window\._JdEid\s*=\s*["\']([^"\']+)["\']',
                r'var\s+_JdEid\s*=\s*["\']([^"\']+)["\']',
                r'_JdEid["\']?\s*[:=]\s*["\']([^"\']+)["\']'
            ]

            for pattern in eid_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    self.eid = match.group(1)
                    print(f"✅ 从JavaScript获取到_JdEid: {self.eid[:20]}...")
                    break

        # 查找 _JdJrTdRiskFpInfo 变量
        if not self.fp:
            # 多种可能的_JdJrTdRiskFpInfo模式
            fp_patterns = [
                r'_JdJrTdRiskFpInfo\s*=\s*["\']([^"\']+)["\']',
                r'window\._JdJrTdRiskFpInfo\s*=\s*["\']([^"\']+)["\']',
                r'var\s+_JdJrTdRiskFpInfo\s*=\s*["\']([^"\']+)["\']',
                r'_JdJrTdRiskFpInfo["\']?\s*[:=]\s*["\']([^"\']+)["\']'
            ]

            for pattern in fp_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    self.fp = match.group(1)
                    print(f"✅ 从JavaScript获取到_JdJrTdRiskFpInfo: {self.fp[:20]}...")
                    break
    
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
        import time
        import hashlib

        # 基于时间戳和随机数生成更真实的eid
        timestamp = str(int(time.time() * 1000))
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        # 生成足够长的随机部分
        random_part1 = ''.join(random.choice(chars) for _ in range(30))
        random_part2 = ''.join(random.choice(chars) for _ in range(30))

        # 生成基于机器特征的部分
        machine_info = f"{timestamp}{random_part1}"
        hash_part = hashlib.md5(machine_info.encode()).hexdigest().upper()[:16]

        # 确保eid长度足够（至少80个字符）
        eid = f"JD_Cartmain_{timestamp}_{hash_part}_{random_part1}_{random_part2}"

        # 如果长度不够，补充随机字符
        while len(eid) < 80:
            eid += random.choice(chars)

        return eid

    def _generate_fp(self):
        """生成fp参数"""
        import time
        import hashlib

        # 基于时间戳和随机数生成更真实的fp
        timestamp = str(int(time.time() * 1000))
        chars = '0123456789abcdef'
        random_part = ''.join(random.choice(chars) for _ in range(16))

        # 生成基于机器特征的指纹
        machine_info = f"{timestamp}{random_part}"
        fp = hashlib.md5(machine_info.encode()).hexdigest()

        return fp
    
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
        # 清理引号
        if self.eid:
            self.eid = self.eid.strip('"\'')
        if self.fp:
            self.fp = self.fp.strip('"\'')

        # 检查eid
        if not self.eid or len(self.eid) < 10:
            print("⚠️ eid参数可能无效：长度不足")
            return False

        # 检查是否是默认测试值
        if self.eid and "AESXKQVW3XZJQVZJXZJQVZJ" in self.eid:
            print("⚠️ eid参数可能无效：检测到默认测试值")
            return False

        # 检查fp
        if not self.fp or len(self.fp) < 16:
            print("⚠️ fp参数可能无效：长度不足")
            return False

        # 检查是否是默认测试值
        if self.fp and self.fp == "b1f2c3d4e5f6a7b8c9d0e1f2a3b4c5d6":
            print("⚠️ fp参数可能无效：检测到默认测试值")
            return False

        print("✅ 设备参数验证通过")
        return True
