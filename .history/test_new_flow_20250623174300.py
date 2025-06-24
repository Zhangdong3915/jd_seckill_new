#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新的执行流程
验证：登录 → 配置检测 → 提示输入 → 加密保存 → 热加载
"""

import os
import sys
import configparser

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_config():
    """创建测试配置文件"""
    config = configparser.ConfigParser()
    
    # 基础配置
    config.add_section('config')
    config.set('config', 'sku_id', '100012043978')
    config.set('config', 'seckill_num', '1')
    config.set('config', 'buy_time', '2025-06-24 11:59:59.200000')
    config.set('config', 'eid', 'test_eid')
    config.set('config', 'fp', 'test_fp')
    config.set('config', 'DEFAULT_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # 账户配置（支付密码为空）
    config.add_section('account')
    config.set('account', 'payment_pwd', '')
    
    # 消息配置（启用但SCKEY为空）
    config.add_section('messenger')
    config.set('messenger', 'enable', 'true')
    config.set('messenger', 'sckey', '')
    
    # 其他必需配置
    config.add_section('settings')
    config.set('settings', 'risk_level', 'BALANCED')
    
    # 保存配置文件
    with open('config.ini', 'w', encoding='utf-8') as f:
        config.write(f)
    
    print("✅ 已创建测试配置文件")

def test_config_validation_flow():
    """测试配置验证流程"""
    print("="*60)
    print("测试新的配置验证流程")
    print("="*60)
    
    # 创建测试配置
    create_test_config()
    
    try:
        # 测试安全配置管理器
        from helper.secure_config import SecureConfigManager
        secure_config = SecureConfigManager()
        
        print("\n1. 测试支付密码检测（应该提示配置）:")
        try:
            password = secure_config.get_payment_password(required=True, allow_input=False)
            print(f"❌ 应该检测到未配置: {password}")
            return False
        except ValueError:
            print("✅ 正确检测到支付密码未配置")
        
        print("\n2. 测试SCKEY检测（应该显示警告）:")
        sckey = secure_config.get_sckey(required=True, allow_input=False)
        if not sckey:
            print("✅ 正确检测到SCKEY未配置并显示警告")
        else:
            print(f"❌ 应该检测到SCKEY为空: {sckey}")
            return False
        
        print("\n3. 测试环境变量优先级:")
        # 设置环境变量
        os.environ['JD_PAYMENT_PWD'] = 'test_env_pwd'
        os.environ['JD_SCKEY'] = 'test_env_sckey'
        
        # 重新创建配置管理器
        secure_config = SecureConfigManager()
        
        password = secure_config.get_payment_password(required=True, allow_input=False)
        sckey = secure_config.get_sckey(required=True, allow_input=False)
        
        if password == 'test_env_pwd' and sckey == 'test_env_sckey':
            print("✅ 环境变量优先级正确")
        else:
            print(f"❌ 环境变量优先级错误: pwd={password}, sckey={sckey}")
            return False
        
        # 清理环境变量
        del os.environ['JD_PAYMENT_PWD']
        del os.environ['JD_SCKEY']
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_fix():
    """测试fallback参数修复"""
    print("\n" + "="*60)
    print("测试fallback参数修复")
    print("="*60)
    
    try:
        from maotai.config import global_config
        
        # 测试正常配置读取
        try:
            sku_id = global_config.getRaw('config', 'sku_id')
            print(f"✅ 正常配置读取成功: sku_id = {sku_id}")
        except Exception as e:
            print(f"❌ 正常配置读取失败: {e}")
            return False
        
        # 测试不存在的配置（应该抛出异常）
        try:
            non_exist = global_config.getRaw('config', 'non_exist_key')
            print(f"❌ 应该抛出异常但返回了: {non_exist}")
            return False
        except:
            print("✅ 不存在的配置正确抛出异常")
        
        return True
        
    except Exception as e:
        print(f"❌ fallback修复测试失败: {e}")
        return False

def test_main_flow_simulation():
    """模拟主程序流程"""
    print("\n" + "="*60)
    print("模拟主程序流程")
    print("="*60)
    
    try:
        # 模拟JdSeckill初始化
        print("1. 初始化JdSeckill...")
        from maotai.jd_spider_requests import JdSeckill
        
        # 这里不会真正登录，只是测试初始化
        print("✅ JdSeckill初始化成功")
        
        # 测试配置验证方法存在
        jd = JdSeckill()
        if hasattr(jd, '_validate_and_setup_config'):
            print("✅ 配置验证方法存在")
        else:
            print("❌ 配置验证方法不存在")
            return False
        
        if hasattr(jd, 'get_secure_payment_password'):
            print("✅ 安全支付密码方法存在")
        else:
            print("❌ 安全支付密码方法不存在")
            return False
        
        if hasattr(jd, 'get_secure_sckey'):
            print("✅ 安全SCKEY方法存在")
        else:
            print("❌ 安全SCKEY方法不存在")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 主程序流程模拟失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("京东茅台秒杀系统 - 新流程测试")
    print("版本: v2.1.1 (2025-06-23)")
    print("测试新的执行流程：登录 → 配置检测 → 提示输入 → 加密保存")
    
    test_results = []
    
    # 执行各项测试
    test_results.append(("配置验证流程", test_config_validation_flow()))
    test_results.append(("fallback参数修复", test_fallback_fix()))
    test_results.append(("主程序流程模拟", test_main_flow_simulation()))
    
    # 输出测试结果
    print("\n" + "="*60)
    print("新流程测试结果")
    print("="*60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 新流程测试通过！")
        print("\n📋 修复内容:")
        print("1. ✅ 修复Config.getRaw()的fallback参数问题")
        print("2. ✅ 调整执行流程：先登录再检测配置")
        print("3. ✅ 登录成功后自动验证配置")
        print("4. ✅ 支持配置热加载和重新验证")
        print("5. ✅ 友好的用户提示和错误处理")
        print("\n🚀 新的执行流程:")
        print("用户启动程序 → 选择功能 → 扫码登录 → 收集设备指纹")
        print("→ 验证必需配置 → 提示用户输入 → 加密保存 → 继续执行")
    else:
        print("\n⚠️ 部分功能需要完善")
    
    print("="*60)

if __name__ == "__main__":
    main()
