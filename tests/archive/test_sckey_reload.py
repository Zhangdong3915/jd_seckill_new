#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试SCKEY配置后立即生效的功能
"""

import sys
import os

def test_sckey_immediate_effect():
    """测试SCKEY配置后立即生效"""
    print("SCKEY配置立即生效测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from helper.secure_config import SecureConfigManager
        
        print("🔧 初始化测试环境...")
        
        # 创建JdSeckill实例
        jd = JdSeckill()
        
        print("📱 测试SCKEY配置前的状态...")
        
        # 检查当前SCKEY配置
        if jd.secure_config:
            current_sckey = jd.secure_config.get_secure_value(
                section='messenger',
                key='sckey',
                env_var_name='JD_SCKEY',
                prompt_text=None,
                allow_input=False
            )
            print(f"当前SCKEY: {current_sckey[:10]}...{current_sckey[-10:] if current_sckey and len(current_sckey) > 20 else current_sckey}")
        
        # 模拟配置SCKEY的过程
        print("\n🔧 模拟SCKEY配置过程...")
        
        # 重置配置状态，模拟首次配置
        jd.config_setup_completed['wechat_notification'] = False
        
        # 调用微信通知配置函数
        print("调用微信通知配置函数...")
        jd._setup_wechat_notification()
        
        print("\n📱 测试SCKEY配置后的状态...")
        
        # 再次检查SCKEY配置
        if jd.secure_config:
            new_sckey = jd.secure_config.get_secure_value(
                section='messenger',
                key='sckey',
                env_var_name='JD_SCKEY',
                prompt_text=None,
                allow_input=False
            )
            print(f"新的SCKEY: {new_sckey[:10]}...{new_sckey[-10:] if new_sckey and len(new_sckey) > 20 else new_sckey}")
            
            if new_sckey:
                print("✅ SCKEY配置成功，现在测试通知发送...")
                
                # 测试发送通知
                jd.nick_name = "测试用户"
                jd.send_notification("配置测试", "SCKEY配置后立即生效测试", "success")
                
                print("✅ 通知发送测试完成")
                return True
            else:
                print("❌ SCKEY配置失败或用户选择跳过")
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
        print("京东茅台秒杀系统 - SCKEY配置立即生效测试")
        print("=" * 60)
        
        # 执行测试
        success = test_sckey_immediate_effect()
        
        if success:
            print("\n🎉 SCKEY配置立即生效测试成功！")
            print("如果您收到了微信通知，说明SCKEY配置后能立即生效")
        else:
            print("\n❌ SCKEY配置立即生效测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
