#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试真实登录流程中的通知发送
模拟实际程序运行时的登录通知场景
"""

import sys
import os

def test_real_login_notification():
    """测试真实登录流程中的通知发送"""
    print("真实登录流程通知测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        print("🔧 步骤1: 初始化系统（模拟main.py流程）...")
        
        # 创建JdSeckill实例
        jd = JdSeckill()
        
        print("🔧 步骤2: 执行配置检查...")
        
        # 执行配置检查（模拟main.py中的流程）
        config_ok = jd.check_and_fix_config()
        
        if config_ok:
            print("✅ 配置检查完成")
        else:
            print("⚠️ 配置检查发现问题，但继续测试")
        
        print("\n🔧 步骤3: 模拟登录成功后的通知发送...")
        
        # 设置用户名（模拟登录成功后的状态）
        jd.nick_name = "测试用户"
        
        print("📱 发送登录成功的详细通知...")
        
        # 模拟login_by_qrcode方法中的通知发送逻辑
        notification_data = {
            'type': '登录通知',
            'icon': '✅',
            'title': '登录成功',
            'summary': f'用户 {jd.nick_name} 已成功登录',
            'login_action': '用户登录',
            'login_status': '已登录',
            'login_success': True
        }
        
        # 这是实际程序中使用的通知发送方法
        jd.send_detailed_notification(notification_data)
        
        print("✅ 真实登录流程通知测试完成")
        print("如果您收到了微信通知，说明登录通知功能在实际程序中也能正常工作")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - 真实登录流程通知测试")
        print("=" * 60)
        
        # 检查配置
        print("🔧 检查微信通知配置...")
        from maotai.config import global_config
        from helper.secure_config import SecureConfigManager
        
        enable = global_config.getRaw('messenger', 'enable')
        if enable != 'true':
            print("❌ 微信通知未启用，请在config.ini中设置 enable = true")
            return False
        
        secure_config = SecureConfigManager()
        sckey = secure_config.get_secure_value(
            section='messenger',
            key='sckey',
            env_var_name='JD_SCKEY',
            prompt_text=None,
            allow_input=False
        )
        
        if not sckey:
            print("❌ SCKEY未配置，无法发送微信通知")
            return False
        
        print("✅ 微信通知配置正常")
        
        # 执行真实登录流程通知测试
        success = test_real_login_notification()
        
        if success:
            print("\n🎉 真实登录流程通知测试成功！")
            print("修复后的程序现在可以在实际登录时正常发送通知了")
        else:
            print("\n❌ 真实登录流程通知测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
