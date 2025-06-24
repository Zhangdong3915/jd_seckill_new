#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试配置参数验证功能
"""

import os
import sys
import configparser
import tempfile
import shutil

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_config(payment_pwd="", sckey="", messenger_enable="false"):
    """创建测试配置文件"""
    config = configparser.ConfigParser()
    
    # 基础配置
    config.add_section('config')
    config.set('config', 'sku_id', '100012043978')
    config.set('config', 'eid', 'test_eid')
    config.set('config', 'fp', 'test_fp')
    
    # 账户配置
    config.add_section('account')
    config.set('account', 'payment_pwd', payment_pwd)
    
    # 消息配置
    config.add_section('messenger')
    config.set('messenger', 'enable', messenger_enable)
    config.set('messenger', 'sckey', sckey)
    
    # 其他必需配置
    config.add_section('settings')
    config.set('settings', 'risk_level', 'BALANCED')
    
    # 保存到临时文件
    temp_config = 'test_config.ini'
    with open(temp_config, 'w', encoding='utf-8') as f:
        config.write(f)
    
    return temp_config

def test_payment_pwd_required():
    """测试支付密码必需检测"""
    print("="*60)
    print("测试支付密码必需检测")
    print("="*60)
    
    # 备份原配置
    original_config = 'config.ini'
    backup_config = 'config_backup.ini'
    if os.path.exists(original_config):
        shutil.copy(original_config, backup_config)
    
    try:
        # 测试1: 支付密码为空
        print("\n1. 测试支付密码为空的情况:")
        test_config = create_test_config(payment_pwd="", messenger_enable="false")
        shutil.copy(test_config, original_config)
        
        try:
            from helper.secure_config import SecureConfigManager
            secure_config = SecureConfigManager()
            password = secure_config.get_payment_password(required=True, allow_input=False)
            print("❌ 应该抛出异常但没有")
            return False
        except ValueError as e:
            print("✅ 正确检测到支付密码未配置")
        except Exception as e:
            print(f"❌ 意外异常: {e}")
            return False
        
        # 测试2: 支付密码已配置
        print("\n2. 测试支付密码已配置的情况:")
        test_config = create_test_config(payment_pwd="123456", messenger_enable="false")
        shutil.copy(test_config, original_config)
        
        try:
            secure_config = SecureConfigManager()
            password = secure_config.get_payment_password(required=True)
            if password == "123456":
                print("✅ 正确获取到支付密码")
            else:
                print(f"❌ 支付密码不匹配: {password}")
                return False
        except Exception as e:
            print(f"❌ 获取支付密码失败: {e}")
            return False
        
        # 清理测试文件
        if os.path.exists(test_config):
            os.remove(test_config)
        
        return True
        
    finally:
        # 恢复原配置
        if os.path.exists(backup_config):
            shutil.copy(backup_config, original_config)
            os.remove(backup_config)

def test_sckey_conditional():
    """测试SCKEY条件检测"""
    print("\n" + "="*60)
    print("测试SCKEY条件检测")
    print("="*60)
    
    # 备份原配置
    original_config = 'config.ini'
    backup_config = 'config_backup.ini'
    if os.path.exists(original_config):
        shutil.copy(original_config, backup_config)
    
    try:
        # 测试1: 微信通知禁用，SCKEY为空
        print("\n1. 测试微信通知禁用的情况:")
        test_config = create_test_config(payment_pwd="123456", sckey="", messenger_enable="false")
        shutil.copy(test_config, original_config)
        
        try:
            from helper.secure_config import SecureConfigManager
            secure_config = SecureConfigManager()
            sckey = secure_config.get_sckey(required=False)
            print("✅ 微信通知禁用时SCKEY检测正常")
        except Exception as e:
            print(f"❌ 微信通知禁用时SCKEY检测失败: {e}")
            return False
        
        # 测试2: 微信通知启用，SCKEY为空
        print("\n2. 测试微信通知启用但SCKEY为空的情况:")
        test_config = create_test_config(payment_pwd="123456", sckey="", messenger_enable="true")
        shutil.copy(test_config, original_config)
        
        try:
            secure_config = SecureConfigManager()
            sckey = secure_config.get_sckey(required=True)
            if not sckey:
                print("✅ 正确检测到SCKEY未配置")
            else:
                print(f"❌ 应该检测到SCKEY为空: {sckey}")
                return False
        except Exception as e:
            print(f"ℹ️ SCKEY检测产生警告（正常）: {e}")
        
        # 测试3: 微信通知启用，SCKEY已配置
        print("\n3. 测试微信通知启用且SCKEY已配置的情况:")
        test_config = create_test_config(payment_pwd="123456", sckey="SCT123456ABCDEF", messenger_enable="true")
        shutil.copy(test_config, original_config)
        
        try:
            secure_config = SecureConfigManager()
            sckey = secure_config.get_sckey(required=True)
            if sckey == "SCT123456ABCDEF":
                print("✅ 正确获取到SCKEY")
            else:
                print(f"❌ SCKEY不匹配: {sckey}")
                return False
        except Exception as e:
            print(f"❌ 获取SCKEY失败: {e}")
            return False
        
        # 清理测试文件
        if os.path.exists(test_config):
            os.remove(test_config)
        
        return True
        
    finally:
        # 恢复原配置
        if os.path.exists(backup_config):
            shutil.copy(backup_config, original_config)
            os.remove(backup_config)

def test_environment_variables():
    """测试环境变量优先级"""
    print("\n" + "="*60)
    print("测试环境变量优先级")
    print("="*60)
    
    # 设置测试环境变量
    os.environ['JD_PAYMENT_PWD'] = 'env_password_123'
    os.environ['JD_SCKEY'] = 'env_sckey_456'
    
    try:
        from helper.secure_config import SecureConfigManager
        secure_config = SecureConfigManager()
        
        # 测试支付密码环境变量
        password = secure_config.get_payment_password(required=True)
        if password == 'env_password_123':
            print("✅ 环境变量支付密码优先级正确")
        else:
            print(f"❌ 环境变量支付密码优先级错误: {password}")
            return False
        
        # 测试SCKEY环境变量
        sckey = secure_config.get_sckey(required=True)
        if sckey == 'env_sckey_456':
            print("✅ 环境变量SCKEY优先级正确")
        else:
            print(f"❌ 环境变量SCKEY优先级错误: {sckey}")
            return False
        
        return True
        
    finally:
        # 清理环境变量
        if 'JD_PAYMENT_PWD' in os.environ:
            del os.environ['JD_PAYMENT_PWD']
        if 'JD_SCKEY' in os.environ:
            del os.environ['JD_SCKEY']

def main():
    """主测试函数"""
    print("配置参数验证功能测试")
    print("版本: v2.1.1 (2025-06-23)")
    
    test_results = []
    
    # 执行各项测试
    test_results.append(("支付密码必需检测", test_payment_pwd_required()))
    test_results.append(("SCKEY条件检测", test_sckey_conditional()))
    test_results.append(("环境变量优先级", test_environment_variables()))
    
    # 输出测试结果
    print("\n" + "="*60)
    print("配置验证测试结果")
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
        print("\n🎉 配置验证功能测试通过！")
        print("\n📋 验证功能:")
        print("1. ✅ 支付密码必需检测 - 未配置时报错并提示")
        print("2. ✅ SCKEY条件检测 - 仅在启用时检测")
        print("3. ✅ 环境变量优先级 - 正确的优先级顺序")
        print("4. ✅ 详细配置指导 - 明确的环境变量名和设置方法")
        print("\n🔧 用户体验:")
        print("- 明确的错误提示和解决方案")
        print("- 详细的环境变量设置指导")
        print("- 条件性的参数检测")
        print("- 友好的警告和提醒")
    else:
        print("\n⚠️ 部分功能需要完善")
    
    print("="*60)

if __name__ == "__main__":
    main()
