#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
登录通知测试脚本
测试登录成功后是否能正常发送通知
"""

import sys
import os

def test_login_notification():
    """测试登录通知功能"""
    print("登录通知功能测试")
    print("=" * 60)
    
    try:
        # 导入必要的模块
        from maotai.jd_spider_requests import JdSeckill
        from helper.secure_config import SecureConfigManager

        print("🔧 初始化测试环境...")

        # 创建JdSeckill实例
        jd = JdSeckill()
        
        print("📱 模拟登录成功通知...")
        
        # 模拟登录成功的通知数据
        notification_data = {
            'type': '登录通知',
            'icon': '✅',
            'title': '登录成功',
            'summary': '测试用户已成功登录',
            'login_action': '用户登录',
            'login_status': '已登录',
            'login_success': True
        }
        
        # 设置测试用户名
        spider.nick_name = "测试用户"
        
        # 发送详细通知
        print("发送详细登录通知...")
        spider.send_detailed_notification(notification_data)
        
        print("\n发送简单登录通知...")
        spider.send_notification("登录成功", "测试用户已成功登录京东账号", "success")
        
        print("\n✅ 登录通知测试完成")
        print("请检查您的微信是否收到了登录通知消息")
        
        return True
        
    except Exception as e:
        print(f"❌ 登录通知测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - 登录通知测试")
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
        
        # 执行登录通知测试
        success = test_login_notification()
        
        if success:
            print("\n🎉 登录通知功能测试成功！")
            print("如果您收到了微信通知，说明登录通知功能正常工作")
        else:
            print("\n❌ 登录通知功能测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
