#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Server酱微信推送功能
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_wechat_push():
    """测试微信推送功能"""
    print("=" * 60)
    print("Server酱微信推送测试")
    print("=" * 60)
    
    try:
        from helper.jd_helper import send_wechat
        from maotai.config import global_config
        
        # 检查配置
        enable = global_config.getRaw('messenger', 'enable')
        sckey = global_config.getRaw('messenger', 'sckey')
        
        print(f"推送开关: {enable}")
        print(f"SCKEY: {sckey}")
        
        if enable != 'true':
            print("❌ 推送功能未开启，请在config.ini中设置 enable = true")
            return False
        
        if not sckey or sckey.strip() == '':
            print("❌ SCKEY未配置，请在config.ini中设置正确的sckey")
            return False
        
        # 判断Server酱版本
        if sckey.startswith('SCT'):
            print("✅ 检测到新版Server酱Turbo")
            api_url = f"https://sctapi.ftqq.com/{sckey}.send"
        else:
            print("✅ 检测到旧版Server酱")
            api_url = f"http://sc.ftqq.com/{sckey}.send"
        
        print(f"API地址: {api_url}")
        
        # 发送测试消息
        print("\n发送测试消息...")
        test_message = """
🎯 京东秒杀系统测试通知

这是一条测试消息，用于验证Server酱推送功能是否正常工作。

测试时间: 2025-06-20 17:00:00
测试内容: 微信推送功能验证
系统状态: 正常运行

如果您收到这条消息，说明推送功能配置正确！
        """
        
        send_wechat(test_message.strip())
        
        print("✅ 测试消息已发送")
        print("\n请检查您的微信是否收到推送消息")
        print("如果没有收到，请检查以下几点：")
        print("1. SCKEY是否正确")
        print("2. Server酱服务是否正常")
        print("3. 微信是否关注了Server酱公众号")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """测试配置读取"""
    print("\n" + "=" * 60)
    print("配置检查")
    print("=" * 60)
    
    try:
        from maotai.config import global_config
        
        # 读取所有messenger配置
        try:
            enable = global_config.getRaw('messenger', 'enable')
            sckey = global_config.getRaw('messenger', 'sckey')
            
            print("当前配置:")
            print(f"  enable = {enable}")
            print(f"  sckey = {sckey}")
            
            # 验证配置
            issues = []
            
            if enable not in ['true', 'false']:
                issues.append("enable 应该设置为 true 或 false")
            
            if enable == 'true':
                if not sckey or sckey.strip() == '':
                    issues.append("启用推送时必须配置 sckey")
                elif not (sckey.startswith('SCT') or len(sckey) > 10):
                    issues.append("sckey 格式可能不正确")
            
            if issues:
                print("\n❌ 配置问题:")
                for issue in issues:
                    print(f"  • {issue}")
                return False
            else:
                print("\n✅ 配置检查通过")
                return True
                
        except Exception as e:
            print(f"❌ 读取配置失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 配置模块加载失败: {e}")
        return False

def test_api_connectivity():
    """测试API连通性"""
    print("\n" + "=" * 60)
    print("API连通性测试")
    print("=" * 60)
    
    try:
        import requests
        from maotai.config import global_config
        
        sckey = global_config.getRaw('messenger', 'sckey')
        
        if sckey.startswith('SCT'):
            url = f"https://sctapi.ftqq.com/{sckey}.send"
        else:
            url = f"http://sc.ftqq.com/{sckey}.send"
        
        print(f"测试URL: {url}")
        
        # 发送一个简单的测试请求
        payload = {
            "text": "连通性测试",
            "desp": "这是一个API连通性测试消息"
        }
        
        print("发送测试请求...")
        resp = requests.get(url, params=payload, timeout=10)
        
        print(f"响应状态码: {resp.status_code}")
        print(f"响应头: {dict(resp.headers)}")
        
        if resp.status_code == 200:
            try:
                result = resp.json()
                print(f"响应内容: {result}")
                
                if result.get('code') == 0:
                    print("✅ API连通性测试成功")
                    return True
                else:
                    print(f"❌ API返回错误: {result.get('message', '未知错误')}")
                    return False
            except:
                print("⚠️ 响应不是JSON格式，但状态码正常")
                print(f"响应内容: {resp.text[:200]}")
                return True
        else:
            print(f"❌ API连通性测试失败，状态码: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API连通性测试异常: {e}")
        return False

def main():
    """主测试函数"""
    try:
        print("Server酱微信推送功能完整测试")
        print("=" * 60)
        
        # 执行测试
        config_ok = test_config()
        api_ok = test_api_connectivity() if config_ok else False
        push_ok = test_wechat_push() if api_ok else False
        
        print("\n" + "=" * 60)
        print("测试结果汇总")
        print("=" * 60)
        print(f"配置检查: {'✅ 通过' if config_ok else '❌ 失败'}")
        print(f"API连通性: {'✅ 通过' if api_ok else '❌ 失败'}")
        print(f"推送功能: {'✅ 通过' if push_ok else '❌ 失败'}")
        
        if config_ok and api_ok and push_ok:
            print("\n🎉 Server酱推送功能完全正常！")
            print("您应该已经收到了测试推送消息")
        else:
            print("\n⚠️ 推送功能存在问题，请根据上述提示进行修复")
            
            if not config_ok:
                print("\n修复建议:")
                print("1. 检查 config.ini 中的 messenger 配置")
                print("2. 确保 enable = true")
                print("3. 确保 sckey 配置正确")
            elif not api_ok:
                print("\n修复建议:")
                print("1. 检查网络连接")
                print("2. 验证 sckey 是否有效")
                print("3. 确认 Server酱服务状态")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
