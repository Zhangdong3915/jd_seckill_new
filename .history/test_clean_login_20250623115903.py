#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理环境并测试基础登录
"""

import sys
import os
import shutil
import time

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def clean_environment():
    """清理可能影响登录的环境"""
    print("🧹 清理环境...")
    
    # 1. 备份并清理Cookie
    cookies_dir = "cookies"
    if os.path.exists(cookies_dir):
        backup_dir = f"cookies_backup_{int(time.time())}"
        try:
            shutil.copytree(cookies_dir, backup_dir)
            print(f"📦 Cookie已备份到: {backup_dir}")
            
            # 清理Cookie文件
            for file in os.listdir(cookies_dir):
                file_path = os.path.join(cookies_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"🗑️ 删除Cookie: {file}")
        except Exception as e:
            print(f"⚠️ Cookie清理失败: {e}")
    
    # 2. 清理可能的缓存文件
    cache_files = ["qr_code.png", "disable_login_check.flag"]
    for file in cache_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ 删除缓存文件: {file}")
    
    print("✅ 环境清理完成")

def test_basic_components():
    """测试基础组件"""
    print("\n🔧 测试基础组件...")
    
    try:
        # 测试网络连接
        import requests
        print("📡 测试网络连接...")
        
        test_urls = [
            "https://www.jd.com",
            "https://passport.jd.com", 
            "https://order.jd.com"
        ]
        
        for url in test_urls:
            try:
                resp = requests.get(url, timeout=5)
                status = "✅ 正常" if resp.status_code == 200 else f"⚠️ {resp.status_code}"
                print(f"   {url}: {status}")
            except Exception as e:
                print(f"   {url}: ❌ 失败 - {str(e)[:50]}")
        
        # 测试配置加载
        print("\n⚙️ 测试配置加载...")
        from maotai.config import global_config
        
        sku_id = global_config.getRaw('config', 'sku_id')
        user_agent = global_config.getRaw('config', 'DEFAULT_USER_AGENT')
        
        print(f"   SKU ID: {sku_id}")
        print(f"   User Agent: {user_agent[:50]}...")
        
        print("✅ 基础组件测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 基础组件测试失败: {e}")
        return False

def test_fresh_login():
    """测试全新登录"""
    print("\n🔐 测试全新登录...")
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        # 创建全新实例
        jd = JdSeckill()
        
        print(f"📊 初始登录状态: {jd.qrlogin.is_login}")
        
        # 测试Cookie验证方法
        print("🍪 测试Cookie验证...")
        cookie_valid = jd.qrlogin._validate_cookies()
        print(f"   Cookie验证结果: {cookie_valid}")
        
        # 检查Session状态
        print("🌐 检查Session状态...")
        cookies = jd.session.cookies
        print(f"   Session Cookie数量: {len(cookies)}")
        
        # 如果没有登录，提示手动登录测试
        if not jd.qrlogin.is_login:
            print("\n💡 建议手动测试登录:")
            print("1. 运行: python main.py")
            print("2. 选择登录功能")
            print("3. 观察登录过程是否正常")
            print("4. 检查是否能获取到二维码")
            print("5. 扫码后观察验证过程")
        
        return True
        
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_config_issues():
    """检查配置问题"""
    print("\n⚙️ 检查配置问题...")
    
    try:
        # 检查eid和fp参数
        from maotai.config import global_config
        
        eid = global_config.getRaw('config', 'eid')
        fp = global_config.getRaw('config', 'fp')
        
        print(f"📋 EID参数: {eid[:20]}...")
        print(f"📋 FP参数: {fp}")
        
        # 检查User-Agent
        user_agent = global_config.getRaw('config', 'DEFAULT_USER_AGENT')
        print(f"🌐 User-Agent: {user_agent}")
        
        # 检查是否是过时的Chrome版本
        if "Chrome/87" in user_agent:
            print("⚠️ 警告: User-Agent使用的是较旧的Chrome版本")
            print("💡 建议: 更新为最新的Chrome User-Agent")
            
            # 提供新的User-Agent
            new_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            print(f"🆕 建议的新User-Agent: {new_ua}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def suggest_fixes():
    """建议修复方案"""
    print("\n" + "="*60)
    print("🔧 建议的修复方案")
    print("="*60)
    
    print("1. 🆕 更新User-Agent")
    print("   在config.ini中更新DEFAULT_USER_AGENT为最新版本")
    
    print("\n2. 🔄 更新eid和fp参数")
    print("   这些参数可能已过期，需要重新获取")
    print("   参考: https://github.com/tychxn/jd-assistant")
    
    print("\n3. 🌐 检查网络环境")
    print("   确保网络连接稳定，没有代理干扰")
    
    print("\n4. 🧹 完全重置")
    print("   删除cookies目录，重新开始登录")
    
    print("\n5. 🔍 逐步调试")
    print("   运行main.py，观察登录过程的每一步")
    print("   特别注意二维码生成和验证步骤")

def main():
    """主函数"""
    print("🔍 登录问题诊断工具")
    print("="*60)
    
    # 1. 清理环境
    clean_environment()
    
    # 2. 测试基础组件
    components_ok = test_basic_components()
    
    # 3. 检查配置
    config_ok = check_config_issues()
    
    # 4. 测试登录
    login_ok = test_fresh_login()
    
    # 5. 总结和建议
    print("\n" + "="*60)
    print("📊 诊断结果")
    print("="*60)
    print(f"基础组件: {'✅ 正常' if components_ok else '❌ 异常'}")
    print(f"配置检查: {'✅ 正常' if config_ok else '❌ 异常'}")
    print(f"登录测试: {'✅ 正常' if login_ok else '❌ 异常'}")
    
    if not all([components_ok, config_ok, login_ok]):
        suggest_fixes()
    else:
        print("\n✅ 所有检查都通过，登录应该可以正常工作")
        print("💡 如果仍有问题，请尝试手动运行 python main.py 进行登录")

if __name__ == "__main__":
    main()
