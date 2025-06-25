#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终测试SCKEY配置和通知发送
验证修复后的完整流程
"""

import sys
import os

def test_sckey_final():
    """最终测试SCKEY配置和通知发送"""
    print("SCKEY配置和通知发送最终测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from helper.jd_helper import send_wechat
        
        print("🔧 初始化系统...")
        jd = JdSeckill()
        
        print("📋 检查当前SCKEY配置状态...")
        
        # 检查当前SCKEY
        if jd.secure_config:
            current_sckey = jd.secure_config.get_secure_value(
                section='messenger',
                key='sckey',
                env_var_name='JD_SCKEY',
                prompt_text=None,
                allow_input=False
            )
            
            if current_sckey:
                print(f"✅ 检测到SCKEY: {current_sckey[:10]}...{current_sckey[-10:]}")
                
                print("\n🧪 测试1: 直接调用send_wechat函数（传递secure_config）...")
                try:
                    send_wechat("测试消息1：使用传递的secure_config参数", jd.secure_config)
                    print("✅ 测试1完成")
                except Exception as e:
                    print(f"❌ 测试1失败: {e}")
                
                print("\n🧪 测试2: 直接调用send_wechat函数（不传递secure_config）...")
                try:
                    send_wechat("测试消息2：使用内部创建的secure_config")
                    print("✅ 测试2完成")
                except Exception as e:
                    print(f"❌ 测试2失败: {e}")
                
                print("\n🧪 测试3: 通过JdSeckill的send_notification方法...")
                try:
                    jd.nick_name = "最终测试用户"
                    jd.send_notification("最终测试", "通过JdSeckill发送的测试通知", "success")
                    print("✅ 测试3完成")
                except Exception as e:
                    print(f"❌ 测试3失败: {e}")
                
                print("\n🧪 测试4: 通过JdSeckill的send_detailed_notification方法...")
                try:
                    notification_data = {
                        'type': '登录通知',
                        'icon': '✅',
                        'title': '最终测试登录成功',
                        'summary': f'用户 {jd.nick_name} 最终测试登录成功',
                        'login_action': '用户登录',
                        'login_status': '已登录',
                        'login_success': True
                    }
                    jd.send_detailed_notification(notification_data)
                    print("✅ 测试4完成")
                except Exception as e:
                    print(f"❌ 测试4失败: {e}")
                
                print("\n✅ 所有测试完成")
                print("请检查您的微信是否收到了4条测试消息")
                return True
                
            else:
                print("❌ 未检测到SCKEY配置")
                return False
        else:
            print("❌ 安全配置管理器未初始化")
            return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - SCKEY配置和通知发送最终测试")
        print("=" * 60)
        print("此测试将验证修复后的完整通知发送流程")
        print("=" * 60)
        
        # 执行测试
        success = test_sckey_final()
        
        if success:
            print("\n🎉 最终测试成功！")
            print("如果您收到了微信通知，说明SCKEY配置和通知发送功能完全正常")
        else:
            print("\n❌ 最终测试失败")
            print("请检查SCKEY配置是否正确")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
