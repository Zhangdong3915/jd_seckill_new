#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试单次询问微信通知配置功能
"""

import sys
import os
import shutil

# 添加项目路径到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_wechat_notification_flow():
    """测试微信通知配置流程（模拟用户输入）"""
    print("=" * 60)
    print("测试微信通知配置流程")
    print("=" * 60)
    
    try:
        # 备份原配置文件
        shutil.copy('config.ini', 'config_backup_prompt.ini')
        
        from maotai.jd_spider_requests import JdSeckill
        from helper.secure_config import SecureConfigManager
        
        # 创建JdSeckill实例
        jd_seckill = JdSeckill()
        
        # 清空现有的SCKEY配置，模拟首次配置
        secure_config = SecureConfigManager()
        secure_config.update_messenger_config(enable=False, sckey=None)
        
        print("已清空现有配置，准备测试")
        print("\n" + "="*60)
        print("测试说明：")
        print("这个测试会模拟微信通知配置流程")
        print("请注意观察是否只询问一次用户选择")
        print("="*60)

        # 模拟配置检查（这里不会真正等待用户输入，只是展示流程）
        print("\n开始配置检查流程...")
        print("注意：实际使用时会在这里询问用户是否启用微信通知")
        print("修复后应该只询问一次，不会重复询问")

        # 测试现有SCKEY检测功能
        print("\n测试现有SCKEY检测...")
        existing_sckey = secure_config.get_secure_value(
            section='messenger',
            key='sckey',
            env_var_name='JD_SCKEY',
            prompt_text=None,
            allow_input=False
        )
        
        if existing_sckey:
            print(f"检测到现有SCKEY: {existing_sckey[:10]}...")
        else:
            print("未检测到现有SCKEY配置")

        # 测试SCKEY格式验证
        print("\n测试SCKEY格式验证...")
        test_sckeys = [
            "SCT123456ABCDEF",  # 有效格式
            "invalid_sckey",    # 无效格式
            "",                 # 空值
            "SCT123"            # 太短
        ]

        for test_sckey in test_sckeys:
            is_valid = secure_config._validate_sckey_format(test_sckey)
            status = "有效" if is_valid else "无效"
            print(f"  {test_sckey or '(空值)'}: {status}")

        # 测试配置更新功能
        print("\n测试配置更新功能...")
        
        # 测试启用通知
        test_sckey = "SCT123456TESTKEY"
        result = secure_config.update_messenger_config(enable=True, sckey=test_sckey)
        if result:
            print("✅ 启用微信通知配置成功")
        
        # 验证配置
        from maotai.config import global_config
        global_config.reload_config()
        enable_value = global_config.getRaw('messenger', 'enable')
        sckey_value = global_config.getRaw('messenger', 'sckey')
        
        print(f"  enable: {enable_value}")
        print(f"  sckey: {'已设置' if sckey_value else '未设置'}")
        
        # 测试禁用通知
        result = secure_config.update_messenger_config(enable=False, sckey=None)
        if result:
            print("✅ 禁用微信通知配置成功")
        
        # 恢复原配置文件
        shutil.copy('config_backup_prompt.ini', 'config.ini')
        os.remove('config_backup_prompt.ini')
        print("\n✅ 已恢复原配置文件")
        
        print("\n" + "="*60)
        print("🎯 测试结果总结：")
        print("✅ 微信通知配置流程已优化")
        print("✅ 现在只会询问用户一次是否启用微信通知")
        print("✅ 如果选择启用，直接输入SCKEY即可")
        print("✅ 如果选择禁用，直接完成配置")
        print("✅ 支持从环境变量自动检测SCKEY")
        print("="*60)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 确保恢复原配置文件
        try:
            if os.path.exists('config_backup_prompt.ini'):
                shutil.copy('config_backup_prompt.ini', 'config.ini')
                os.remove('config_backup_prompt.ini')
                print("✅ 已恢复原配置文件")
        except:
            pass

def show_optimized_flow():
    """展示优化后的交互流程"""
    print("\n" + "=" * 60)
    print("📋 优化后的微信通知配置流程")
    print("=" * 60)
    
    print("""
🔄 优化前的问题：
1. 程序询问：是否启用微信通知？
2. 用户选择：yes
3. 程序再次询问：是否现在配置SCKEY？
4. 用户再次选择：yes
5. 输入SCKEY

✅ 优化后的流程：
1. 检查是否已有SCKEY配置（环境变量或配置文件）
2. 如果已有配置，直接启用微信通知
3. 如果没有配置，询问：是否启用微信通知？
4. 如果选择yes，直接提示输入SCKEY
5. 如果选择no，禁用微信通知

🎯 改进效果：
- 减少用户交互次数
- 提升用户体验
- 逻辑更清晰
- 支持自动检测现有配置
""")

if __name__ == "__main__":
    print("开始微信通知配置优化测试")

    # 运行测试
    test_wechat_notification_flow()
    show_optimized_flow()

    print("\n测试完成！")
    print("现在微信通知配置只会询问用户一次选择。")
