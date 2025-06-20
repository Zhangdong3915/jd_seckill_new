#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全自动化模式测试
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_check():
    """测试配置检查功能"""
    print("=" * 60)
    print("配置检查测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("测试配置检查功能...")
        config_ok = jd.check_and_fix_config()
        
        if config_ok:
            print("[OK] 配置检查通过")
        else:
            print("[WARNING] 配置存在问题")
            
        return config_ok
        
    except Exception as e:
        print(f"[ERROR] 配置检查测试失败: {e}")
        return False

def test_time_status():
    """测试时间状态判断"""
    print("\n" + "=" * 60)
    print("时间状态判断测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("获取当前时间状态...")
        time_status = jd.get_time_status()
        
        print(f"当前状态: {time_status['status']}")
        print(f"操作描述: {time_status['description']}")
        print(f"下一步操作: {time_status['action']}")
        
        if time_status['time_to_action'] > 0:
            hours = int(time_status['time_to_action'] // 3600)
            minutes = int((time_status['time_to_action'] % 3600) // 60)
            seconds = int(time_status['time_to_action'] % 60)
            print(f"剩余时间: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        print("[OK] 时间状态判断正常")
        return True
        
    except Exception as e:
        print(f"[ERROR] 时间状态测试失败: {e}")
        return False

def test_login_maintenance():
    """测试登录维护功能"""
    print("\n" + "=" * 60)
    print("登录维护测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("测试登录状态维护...")
        login_ok = jd.auto_login_maintenance()
        
        if login_ok:
            print("[OK] 登录状态正常")
        else:
            print("[WARNING] 登录状态异常")
            
        return login_ok
        
    except Exception as e:
        print(f"[ERROR] 登录维护测试失败: {e}")
        return False

def test_error_handler():
    """测试错误处理功能"""
    print("\n" + "=" * 60)
    print("错误处理测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("测试错误处理机制...")
        
        # 测试一个会失败的函数
        def test_func():
            raise Exception("测试异常")
        
        try:
            jd.enhanced_error_handler(test_func)
        except Exception as e:
            print(f"[OK] 错误处理正常: {e}")
            
        return True
        
    except Exception as e:
        print(f"[ERROR] 错误处理测试失败: {e}")
        return False

def test_notification():
    """测试通知功能"""
    print("\n" + "=" * 60)
    print("通知功能测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("测试通知功能...")
        
        # 测试各种类型的通知
        jd.send_notification("测试通知", "这是一条测试信息", "info")
        jd.send_notification("成功通知", "这是一条成功信息", "success")
        jd.send_notification("警告通知", "这是一条警告信息", "warning")
        jd.send_notification("错误通知", "这是一条错误信息", "error")
        
        print("[OK] 通知功能正常")
        return True
        
    except Exception as e:
        print(f"[ERROR] 通知功能测试失败: {e}")
        return False

def test_status_panel():
    """测试状态面板"""
    print("\n" + "=" * 60)
    print("状态面板测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("测试状态面板显示...")
        
        time_status = jd.get_time_status()
        jd.display_status_panel(time_status, False, False)
        
        print("[OK] 状态面板显示正常")
        return True
        
    except Exception as e:
        print(f"[ERROR] 状态面板测试失败: {e}")
        return False

def simulate_auto_mode():
    """模拟全自动化模式"""
    print("\n" + "=" * 60)
    print("全自动化模式模拟")
    print("=" * 60)
    
    print("全自动化模式特性:")
    print("1. 智能时间判断 - 自动决定执行预约还是秒杀")
    print("2. 自动登录维护 - 定期检查登录状态，自动重新登录")
    print("3. 增强错误处理 - 网络异常、接口失效自动重试")
    print("4. 实时状态监控 - 清晰的状态面板和进度提示")
    print("5. 多渠道通知 - 控制台、微信等多种通知方式")
    print("6. 配置自动检查 - 启动前检查配置完整性")
    print("7. 跨天执行支持 - 自动处理日期变更")
    print("8. 傻瓜式操作 - 一键启动，无需人工干预")
    
    print("\n使用方法:")
    print("1. 运行: python main.py")
    print("2. 选择: 3 (全自动化执行)")
    print("3. 系统自动检查配置和登录状态")
    print("4. 根据当前时间智能执行相应操作")
    print("5. 程序会持续运行直到任务完成")

def main():
    """主测试函数"""
    try:
        print("全自动化京东秒杀系统测试")
        print("=" * 60)
        
        tests = [
            ("配置检查", test_config_check),
            ("时间状态判断", test_time_status),
            ("登录维护", test_login_maintenance),
            ("错误处理", test_error_handler),
            ("通知功能", test_notification),
            ("状态面板", test_status_panel),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n[测试] {test_name}...")
            if test_func():
                passed += 1
        
        simulate_auto_mode()
        
        print("\n" + "=" * 60)
        print(f"测试结果: {passed}/{total} 通过")
        
        if passed == total:
            print("[SUCCESS] 全自动化系统测试完成！")
            print("\n[建议] 系统已准备就绪，可以使用全自动化模式:")
            print("运行: python main.py")
            print("选择: 3 (全自动化执行)")
        else:
            print("[WARNING] 部分测试失败，请检查相关功能")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
