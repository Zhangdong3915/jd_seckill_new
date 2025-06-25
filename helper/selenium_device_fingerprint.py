#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Selenium设备指纹收集器
使用真实浏览器环境获取京东设备指纹参数
"""

import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException


class SeleniumDeviceFingerprintCollector:
    """使用Selenium收集京东设备指纹"""
    
    def __init__(self, headless=True, timeout=30):
        """
        初始化Selenium设备指纹收集器
        
        Args:
            headless: 是否使用无头模式
            timeout: 超时时间（秒）
        """
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.eid = None
        self.fp = None
        
    def _setup_driver(self):
        """设置Chrome WebDriver"""
        try:
            print("🔧 正在初始化Chrome WebDriver...")
            
            # Chrome选项配置
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
                print("   使用无头模式")
            
            # 基础配置
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript-harmony-shipping')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            
            # 设置用户代理
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            # 窗口大小
            chrome_options.add_argument('--window-size=1920,1080')
            
            # 自动下载ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            # 创建WebDriver实例
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.implicitly_wait(10)
            
            print("✅ Chrome WebDriver初始化成功")
            return True
            
        except Exception as e:
            print(f"❌ Chrome WebDriver初始化失败: {e}")
            return False
    
    def _wait_for_page_load(self, url_contains=""):
        """等待页面加载完成"""
        try:
            # 等待页面加载
            WebDriverWait(self.driver, self.timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # 如果指定了URL包含条件，等待URL匹配
            if url_contains:
                WebDriverWait(self.driver, self.timeout).until(
                    lambda driver: url_contains in driver.current_url
                )
            
            # 额外等待JavaScript执行
            time.sleep(2)
            return True
            
        except TimeoutException:
            print(f"⚠️ 页面加载超时")
            return False
    
    def _extract_device_fingerprint(self):
        """从当前页面提取设备指纹"""
        try:
            print("🔍 正在提取设备指纹参数...")
            
            # 执行JavaScript获取_JdEid
            try:
                eid = self.driver.execute_script("return window._JdEid || '';")
                if eid and len(eid) > 10:
                    self.eid = eid
                    print(f"✅ 获取到_JdEid: {self.eid[:30]}...")
            except Exception as e:
                print(f"⚠️ 获取_JdEid失败: {e}")
            
            # 执行JavaScript获取_JdJrTdRiskFpInfo
            try:
                fp = self.driver.execute_script("return window._JdJrTdRiskFpInfo || '';")
                if fp and len(fp) > 10:
                    self.fp = fp
                    print(f"✅ 获取到_JdJrTdRiskFpInfo: {self.fp[:30]}...")
            except Exception as e:
                print(f"⚠️ 获取_JdJrTdRiskFpInfo失败: {e}")
            
            # 如果直接获取失败，尝试从页面源码中查找
            if not self.eid or not self.fp:
                self._extract_from_page_source()
            
            return self.eid is not None and self.fp is not None
            
        except Exception as e:
            print(f"❌ 提取设备指纹失败: {e}")
            return False
    
    def _extract_from_page_source(self):
        """从页面源码中提取设备指纹"""
        try:
            import re
            page_source = self.driver.page_source
            
            # 查找_JdEid
            if not self.eid:
                eid_patterns = [
                    r'_JdEid\s*=\s*["\']([^"\']+)["\']',
                    r'window\._JdEid\s*=\s*["\']([^"\']+)["\']',
                    r'"_JdEid"\s*:\s*"([^"]+)"'
                ]
                
                for pattern in eid_patterns:
                    match = re.search(pattern, page_source, re.IGNORECASE)
                    if match:
                        self.eid = match.group(1)
                        print(f"✅ 从页面源码获取到_JdEid: {self.eid[:30]}...")
                        break
            
            # 查找_JdJrTdRiskFpInfo
            if not self.fp:
                fp_patterns = [
                    r'_JdJrTdRiskFpInfo\s*=\s*["\']([^"\']+)["\']',
                    r'window\._JdJrTdRiskFpInfo\s*=\s*["\']([^"\']+)["\']',
                    r'"_JdJrTdRiskFpInfo"\s*:\s*"([^"]+)"'
                ]
                
                for pattern in fp_patterns:
                    match = re.search(pattern, page_source, re.IGNORECASE)
                    if match:
                        self.fp = match.group(1)
                        print(f"✅ 从页面源码获取到_JdJrTdRiskFpInfo: {self.fp[:30]}...")
                        break
                        
        except Exception as e:
            print(f"⚠️ 从页面源码提取失败: {e}")
    
    def collect_from_jd_pages(self):
        """从京东页面收集设备指纹"""
        try:
            if not self._setup_driver():
                return None, None
            
            print("🌐 开始访问京东页面收集设备指纹...")
            
            # 页面访问顺序：从最可能包含设备指纹的页面开始
            pages_to_try = [
                ("https://www.jd.com/", "京东首页"),
                ("https://passport.jd.com/new/login.aspx", "登录页面"),
                ("https://cart.jd.com/cart_index", "购物车页面"),
                ("https://item.jd.com/100012043978.html", "茅台商品页面")
            ]
            
            for url, page_name in pages_to_try:
                try:
                    print(f"📱 正在访问{page_name}: {url}")
                    self.driver.get(url)
                    
                    if self._wait_for_page_load():
                        print(f"✅ {page_name}加载完成")
                        
                        # 尝试提取设备指纹
                        if self._extract_device_fingerprint():
                            if self.eid and self.fp:
                                print(f"🎉 从{page_name}成功获取完整设备指纹！")
                                break
                        
                        # 等待一下再尝试下一个页面
                        time.sleep(1)
                    else:
                        print(f"⚠️ {page_name}加载失败")
                        
                except Exception as e:
                    print(f"❌ 访问{page_name}失败: {e}")
                    continue
            
            return self.eid, self.fp
            
        except Exception as e:
            print(f"❌ 收集设备指纹失败: {e}")
            return None, None
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """清理资源"""
        try:
            if self.driver:
                self.driver.quit()
                print("🧹 WebDriver已清理")
        except Exception as e:
            print(f"⚠️ WebDriver清理失败: {e}")
    
    def validate_fingerprint(self, eid, fp):
        """验证设备指纹有效性"""
        if not eid or len(eid) < 10:
            return False, "eid长度不足"
        
        if not fp or len(fp) < 16:
            return False, "fp长度不足"
        
        # 检查是否是默认测试值
        if "AESXKQVW3XZJQVZJXZJQVZJ" in eid:
            return False, "eid是默认测试值"
        
        if fp == "b1f2c3d4e5f6a7b8c9d0e1f2a3b4c5d6":
            return False, "fp是默认测试值"
        
        return True, "验证通过"


def test_selenium_collector():
    """测试Selenium设备指纹收集器"""
    print("Selenium设备指纹收集器测试")
    print("=" * 60)
    
    try:
        # 创建收集器（使用有头模式便于调试）
        collector = SeleniumDeviceFingerprintCollector(headless=False, timeout=30)
        
        # 收集设备指纹
        eid, fp = collector.collect_from_jd_pages()
        
        if eid and fp:
            print(f"\n✅ 设备指纹收集成功:")
            print(f"   eid: {eid}")
            print(f"   fp: {fp}")
            
            # 验证设备指纹
            is_valid, message = collector.validate_fingerprint(eid, fp)
            print(f"   验证结果: {'通过' if is_valid else '失败'} - {message}")
            
            return True
        else:
            print("\n❌ 设备指纹收集失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_selenium_collector()
