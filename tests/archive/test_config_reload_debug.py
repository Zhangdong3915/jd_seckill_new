#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试配置重新加载问题
检查配置重新加载后各个组件的状态
"""

import sys
import os

def debug_config_reload():
    """调试配置重新加载"""
    print("配置重新加载调试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from maotai.config import global_config
        from helper.secure_config import SecureConfigManager
        
        print("🔧 初始化系统...")
        jd = JdSeckill()
        
        print("\n📋 检查初始配置状态...")
        
        # 检查全局配置
        try:
            enable = global_config.getRaw('messenger', 'enable')
            print(f"全局配置 - messenger.enable: {enable}")
        except Exception as e:
            print(f"全局配置读取失败: {e}")
        
        # 检查安全配置
        if jd.secure_config:
            try:
                sckey = jd.secure_config.get_secure_value(
                    section='messenger',
                    key='sckey',
                    env_var_name='JD_SCKEY',
                    prompt_text=None,
                    allow_input=False
                )
                print(f"安全配置 - SCKEY: {sckey[:10]}...{sckey[-10:] if sckey and len(sckey) > 20 else sckey}")
            except Exception as e:
                print(f"安全配置读取失败: {e}")
        
        print("\n🔄 执行配置重新加载...")
        
        # 重新加载配置
        reload_success = jd.reload_config()
        print(f"配置重新加载结果: {reload_success}")
        
        print("\n📋 检查重新加载后的配置状态...")
        
        # 再次检查全局配置
        try:
            enable = global_config.getRaw('messenger', 'enable')
            print(f"全局配置 - messenger.enable: {enable}")
        except Exception as e:
            print(f"全局配置读取失败: {e}")
        
        # 再次检查安全配置
        if jd.secure_config:
            try:
                sckey = jd.secure_config.get_secure_value(
                    section='messenger',
                    key='sckey',
                    env_var_name='JD_SCKEY',
                    prompt_text=None,
                    allow_input=False
                )
                print(f"安全配置 - SCKEY: {sckey[:10]}...{sckey[-10:] if sckey and len(sckey) > 20 else sckey}")
            except Exception as e:
                print(f"安全配置读取失败: {e}")
        
        print("\n🧪 测试通知发送...")
        
        # 测试发送通知
        jd.nick_name = "调试测试用户"
        
        print("发送简单通知...")
        try:
            jd.send_notification("配置调试", "测试配置重新加载后的通知发送", "info")
            print("✅ 简单通知发送完成")
        except Exception as e:
            print(f"❌ 简单通知发送失败: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n📱 直接测试微信推送...")
        
        # 直接测试微信推送
        try:
            from helper.jd_helper import send_wechat
            send_wechat("直接测试微信推送功能\n\n这是一条调试消息，用于验证配置重新加载后微信推送是否正常工作。")
            print("✅ 直接微信推送测试完成")
        except Exception as e:
            print(f"❌ 直接微信推送测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - 配置重新加载调试")
        print("=" * 60)
        
        # 执行调试
        success = debug_config_reload()
        
        if success:
            print("\n✅ 调试完成")
            print("请检查上述输出，查看配置重新加载是否正常")
        else:
            print("\n❌ 调试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 调试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
