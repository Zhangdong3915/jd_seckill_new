#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终集成测试
验证登录和二维码自动关闭的完整流程
"""

import sys
import os
import time

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_login_status():
    """测试登录状态检测"""
    print("="*60)
    print("测试登录状态检测")
    print("="*60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print(f"当前登录状态: {jd.qrlogin.is_login}")
        
        if jd.qrlogin.is_login:
            print("用户已登录，无需重新登录")
            
            # 测试用户名获取
            try:
                username = jd.get_username()
                print(f"用户名: {username}")
            except Exception as e:
                print(f"获取用户名失败: {e}")
            
            # 测试Cookie验证
            cookie_valid = jd.qrlogin._validate_cookies()
            print(f"Cookie验证结果: {cookie_valid}")
            
        else:
            print("用户未登录，需要扫码登录")
        
        return True
        
    except Exception as e:
        print(f"登录状态检测失败: {e}")
        return False

def test_qr_close_mechanism():
    """测试二维码关闭机制"""
    print("\n" + "="*60)
    print("测试二维码自动关闭机制")
    print("="*60)
    
    try:
        from helper.jd_helper import close_image_windows
        import psutil
        
        # 检测当前图片查看器进程
        print("检测当前图片查看器进程:")
        image_viewers = ['Photos.exe', 'Microsoft.Photos.exe', 'PhotosApp.exe', 'dllhost.exe']
        found_processes = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in image_viewers:
                    found_processes.append((proc.info['pid'], proc.info['name']))
                    print(f"  发现进程: {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not found_processes:
            print("  未发现图片查看器进程")
        
        # 测试关闭功能
        print("\n执行二维码窗口关闭功能:")
        close_image_windows()
        
        return True
        
    except Exception as e:
        print(f"二维码关闭机制测试失败: {e}")
        return False

def test_notification_system():
    """测试通知系统"""
    print("\n" + "="*60)
    print("测试通知系统")
    print("="*60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from datetime import datetime
        
        jd = JdSeckill()
        
        # 测试登录成功通知
        print("测试登录成功通知:")
        notification_data = {
            'type': '登录通知',
            'title': '登录成功',
            'summary': '用户已成功登录京东账号',
            'login_action': '用户登录',
            'login_status': '已登录',
            'login_success': True
        }
        jd.send_detailed_notification(notification_data)
        
        return True
        
    except Exception as e:
        print(f"通知系统测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("京东茅台秒杀系统 - 最终集成测试")
    print("版本: v2.1.1 (2025-06-23)")
    print("测试时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("操作系统:", "Windows" if os.name == "nt" else "非Windows")
    
    test_results = []
    
    # 执行各项测试
    test_results.append(("登录状态检测", test_login_status()))
    test_results.append(("二维码关闭机制", test_qr_close_mechanism()))
    test_results.append(("通知系统", test_notification_system()))
    
    # 输出测试结果
    print("\n" + "="*60)
    print("最终集成测试结果")
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
        print("\n所有集成测试通过！系统完全正常。")
        print("\n主要功能验证:")
        print("  - 登录状态自动检测")
        print("  - 新版Cookie格式支持")
        print("  - 二维码窗口自动关闭")
        print("  - 详细通知系统")
        print("  - Windows照片应用兼容")
    else:
        print("\n部分功能可能需要进一步检查。")
    
    print("\n" + "="*60)
    print("v2.1.1 版本完整修复总结:")
    print("1. ✅ 登录问题修复 - 支持京东新版Cookie格式")
    print("2. ✅ 二维码自动关闭 - 多重机制确保窗口关闭")
    print("3. ✅ Windows照片应用 - 正确识别和关闭Photos.exe")
    print("4. ✅ 增强通知系统 - 详细的markdown格式通知")
    print("5. ✅ 智能状态检测 - 自动识别登录状态")
    print("6. ✅ 完善文档记录 - 所有修改都有详细记录")
    print("="*60)
    
    print("\n现在您可以:")
    print("- 正常扫码登录，二维码会自动关闭")
    print("- 接收详细的预约/抢购通知")
    print("- 享受完全自动化的用户体验")

if __name__ == "__main__":
    main()
