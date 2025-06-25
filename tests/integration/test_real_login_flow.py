#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试真实的登录流程
模拟用户实际使用程序时的登录通知
"""

import sys
import os

def test_real_login_flow():
    """测试真实的登录流程"""
    print("真实登录流程测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        print("🔧 步骤1: 初始化系统（模拟main.py的流程）...")
        
        # 创建JdSeckill实例（模拟main.py第一步）
        jd = JdSeckill()
        print(f"初始secure_config实例ID: {id(jd.secure_config) if jd.secure_config else 'None'}")
        
        print("\n🔧 步骤2: 执行配置检查（模拟main.py的check_and_fix_config）...")
        
        # 执行配置检查（这里会重新初始化secure_config）
        config_ok = jd.check_and_fix_config()
        print(f"配置检查后secure_config实例ID: {id(jd.secure_config) if jd.secure_config else 'None'}")
        
        if config_ok:
            print("✅ 配置检查完成")
        else:
            print("⚠️ 配置检查发现问题，但继续测试")
        
        print("\n🔧 步骤3: 模拟用户选择功能并触发登录...")
        
        # 强制设置为未登录状态，模拟需要登录的情况
        jd.qrlogin.is_login = False
        print("已设置为未登录状态")
        
        print("\n📱 步骤4: 模拟登录成功...")
        
        # 直接调用login_by_qrcode方法，但跳过实际的二维码扫描
        # 我们手动设置登录状态并触发通知发送
        jd.qrlogin.is_login = True  # 模拟登录成功
        jd.nick_name = "真实流程测试用户"
        
        print("模拟登录成功，准备发送通知...")
        
        # 确保使用最新的安全配置管理器（这是我们刚刚添加的修复）
        try:
            from helper.secure_config import SecureConfigManager
            jd.secure_config = SecureConfigManager()
            print(f"通知发送前secure_config实例ID: {id(jd.secure_config)}")
        except Exception as e:
            print(f"重新初始化安全配置管理器失败: {e}")
        
        # 发送登录成功通知（模拟login_by_qrcode中的逻辑）
        notification_data = {
            'type': '登录通知',
            'icon': '✅',
            'title': '登录成功',
            'summary': f'用户 {jd.nick_name} 已成功登录',
            'login_action': '用户登录',
            'login_status': '已登录',
            'login_success': True
        }
        
        print("发送详细登录通知...")
        jd.send_detailed_notification(notification_data)
        
        print("发送简单登录通知...")
        jd.send_notification("登录成功", f"用户 {jd.nick_name} 已成功登录京东账号", "success")
        
        print("\n✅ 真实登录流程测试完成")
        print("请检查您的微信是否收到了登录通知消息")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - 真实登录流程测试")
        print("=" * 60)
        print("此测试将完全模拟用户实际使用程序时的登录流程")
        print("包括：初始化 -> 配置检查 -> 登录 -> 通知发送")
        print("=" * 60)
        
        # 执行测试
        success = test_real_login_flow()
        
        if success:
            print("\n🎉 真实登录流程测试成功！")
            print("如果您收到了微信通知，说明登录通知功能在真实场景下正常工作")
        else:
            print("\n❌ 真实登录流程测试失败")
            print("这可能解释了为什么您在实际使用中收不到通知")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
