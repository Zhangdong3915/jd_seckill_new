#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试完整的配置和登录流程
模拟用户首次运行程序的完整体验
"""

import sys
import os

def test_complete_flow():
    """测试完整的配置和登录流程"""
    print("完整配置和登录流程测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        print("🔧 初始化系统...")
        
        # 创建JdSeckill实例（模拟main.py的流程）
        jd = JdSeckill()
        
        print("🔧 执行配置检查...")
        
        # 执行配置检查（这里会询问SCKEY配置）
        config_ok = jd.check_and_fix_config()
        
        if config_ok:
            print("✅ 配置检查完成")
        else:
            print("⚠️ 配置检查发现问题，但继续测试")
        
        print("\n📱 模拟登录成功后发送通知...")
        
        # 模拟登录成功的通知
        jd.nick_name = "测试用户"
        
        # 发送登录成功通知
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
        try:
            jd.send_detailed_notification(notification_data)
            print("✅ 详细通知发送完成")
        except Exception as e:
            print(f"⚠️ 详细通知发送失败: {e}")
        
        print("发送简单登录通知...")
        try:
            jd.send_notification("登录成功", f"用户 {jd.nick_name} 已成功登录京东账号", "success")
            print("✅ 简单通知发送完成")
        except Exception as e:
            print(f"⚠️ 简单通知发送失败: {e}")
        
        print("\n✅ 完整流程测试完成")
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
        print("京东茅台秒杀系统 - 完整配置和登录流程测试")
        print("=" * 60)
        print("此测试将模拟用户首次运行程序的完整体验")
        print("包括配置检查、SCKEY设置、登录通知等")
        print("=" * 60)
        
        # 执行测试
        success = test_complete_flow()
        
        if success:
            print("\n🎉 完整流程测试成功！")
            print("如果您收到了微信通知，说明配置和通知功能正常工作")
        else:
            print("\n❌ 完整流程测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
