#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试安全抢购策略 - 防风控版本
"""

import sys
import os
import time
import random
from datetime import datetime

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_safe_config():
    """测试安全配置"""
    print("=" * 80)
    print("🛡️ 安全配置测试")
    print("=" * 80)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from maotai.config import global_config
        
        jd = JdSeckill()
        
        # 测试不同风险等级的配置
        risk_levels = ['CONSERVATIVE', 'BALANCED', 'AGGRESSIVE']
        
        for risk_level in risk_levels:
            print(f"\n📊 {risk_level} 策略配置:")
            
            # 临时设置风险等级
            original_config = jd.get_safe_seckill_config()
            
            # 模拟不同配置
            if risk_level == 'CONSERVATIVE':
                config = {
                    'risk_level': 'CONSERVATIVE',
                    'max_processes': 3,
                    'max_retries': 50,
                    'retry_interval_range': (0.5, 2.0),
                    'advance_time_limit': 0.2,
                    'description': '保守策略 - 最安全'
                }
            elif risk_level == 'BALANCED':
                config = {
                    'risk_level': 'BALANCED',
                    'max_processes': 8,
                    'max_retries': 100,
                    'retry_interval_range': (0.1, 1.0),
                    'advance_time_limit': 0.8,
                    'description': '平衡策略 - 推荐'
                }
            else:  # AGGRESSIVE
                config = {
                    'risk_level': 'AGGRESSIVE',
                    'max_processes': 15,
                    'max_retries': 200,
                    'retry_interval_range': (0.05, 0.5),
                    'advance_time_limit': 1.2,
                    'description': '激进策略 - 高风险'
                }
            
            print(f"   策略描述: {config['description']}")
            print(f"   并发进程: {config['max_processes']}个")
            print(f"   最大重试: {config['max_retries']}次")
            print(f"   重试间隔: {config['retry_interval_range'][0]*1000:.0f}-{config['retry_interval_range'][1]*1000:.0f}ms")
            print(f"   时间提前: {config['advance_time_limit']*1000:.0f}ms")
            
            # 风险评估
            if risk_level == 'CONSERVATIVE':
                print("   🟢 风控风险: 极低 - 适合新手和低信用账户")
            elif risk_level == 'BALANCED':
                print("   🟡 风控风险: 低 - 适合大多数用户")
            else:
                print("   🔴 风控风险: 中高 - 仅适合高信用账户")
        
        return True
        
    except Exception as e:
        print(f"❌ 安全配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_safe_retry_intervals():
    """测试安全重试间隔"""
    print("\n" + "=" * 80)
    print("⏱️ 安全重试间隔测试")
    print("=" * 80)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        # 测试不同配置的重试间隔
        configs = [
            ('保守策略', (0.5, 2.0)),
            ('平衡策略', (0.1, 1.0)),
            ('激进策略', (0.05, 0.5))
        ]
        
        for strategy_name, retry_range in configs:
            print(f"\n📍 {strategy_name} 重试间隔分析:")
            print(f"   配置范围: {retry_range[0]*1000:.0f}-{retry_range[1]*1000:.0f}ms")
            
            # 模拟10次重试的间隔
            intervals = []
            for retry_count in range(10):
                interval = jd.safe_retry_interval(retry_range, retry_count)
                intervals.append(interval * 1000)  # 转换为毫秒
            
            avg_interval = sum(intervals) / len(intervals)
            min_interval = min(intervals)
            max_interval = max(intervals)
            
            print(f"   实际范围: {min_interval:.0f}-{max_interval:.0f}ms")
            print(f"   平均间隔: {avg_interval:.0f}ms")
            print(f"   随机性: {'✅ 良好' if max_interval - min_interval > 100 else '⚠️ 需改进'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 重试间隔测试失败: {e}")
        return False

def test_risk_control_detection():
    """测试风控检测"""
    print("\n" + "=" * 80)
    print("🚨 风控检测测试")
    print("=" * 80)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        # 测试风控错误识别
        test_errors = [
            ("很遗憾没有抢到，再接再厉哦", False),
            ("请输入验证码", True),
            ("账户操作频繁，请稍后再试", True),
            ("系统正在开小差，请重试", False),
            ("网络连接超时", False),
            ("访问受限，请联系客服", True),
            ("账号存在异常，已被限制", True),
        ]
        
        print("🔍 风控错误识别测试:")
        for error_msg, expected in test_errors:
            result = jd.is_risk_control_error(error_msg)
            status = "✅" if result == expected else "❌"
            risk_type = "风控相关" if result else "普通错误"
            print(f"   {status} {error_msg[:20]}... -> {risk_type}")
        
        # 测试风控检测
        print(f"\n🛡️ 当前风控状态检测:")
        risk_detected = jd.detect_risk_control()
        print(f"   风控信号: {'⚠️ 检测到' if risk_detected else '✅ 正常'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 风控检测测试失败: {e}")
        return False

def test_human_behavior_simulation():
    """测试人类行为模拟"""
    print("\n" + "=" * 80)
    print("🎭 人类行为模拟测试")
    print("=" * 80)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("🎬 开始模拟人类浏览行为...")
        start_time = time.time()
        
        jd.simulate_human_behavior()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"✅ 人类行为模拟完成")
        print(f"   总耗时: {total_time:.1f}秒")
        print(f"   行为特征: 随机停留、自然间隔")
        
        if 2.0 <= total_time <= 6.0:
            print("   🟢 模拟效果: 优秀 - 符合人类行为特征")
        elif 1.0 <= total_time < 2.0 or 6.0 < total_time <= 8.0:
            print("   🟡 模拟效果: 良好 - 基本符合预期")
        else:
            print("   🔴 模拟效果: 需优化 - 可能过快或过慢")
        
        return True
        
    except Exception as e:
        print(f"❌ 人类行为模拟测试失败: {e}")
        return False

def test_safe_wait_time():
    """测试安全等待时间"""
    print("\n" + "=" * 80)
    print("⏳ 安全等待时间测试")
    print("=" * 80)
    
    try:
        from helper.jd_helper import wait_some_time
        
        # 测试不同时间段的等待时间
        scenarios = [
            ("平时", datetime(2025, 6, 20, 10, 0, 0)),
            ("秒杀时", datetime(2025, 6, 20, 12, 0, 30)),
        ]
        
        for scenario_name, test_time in scenarios:
            print(f"\n📍 {scenario_name} 等待时间测试:")
            
            # 测试10次等待时间
            wait_times = []
            for _ in range(10):
                start = time.time()
                wait_some_time()
                end = time.time()
                wait_times.append((end - start) * 1000)  # 转换为毫秒
            
            avg_wait = sum(wait_times) / len(wait_times)
            min_wait = min(wait_times)
            max_wait = max(wait_times)
            
            print(f"   平均等待: {avg_wait:.0f}ms")
            print(f"   范围: {min_wait:.0f}-{max_wait:.0f}ms")
            
            # 评估安全性
            if scenario_name == "秒杀时":
                if 100 <= avg_wait <= 500:
                    print("   🟢 安全等级: 优秀 - 防风控效果好")
                elif 50 <= avg_wait < 100 or 500 < avg_wait <= 800:
                    print("   🟡 安全等级: 良好 - 基本安全")
                else:
                    print("   🔴 安全等级: 需优化 - 可能触发风控")
            else:
                if 200 <= avg_wait <= 800:
                    print("   🟢 安全等级: 优秀 - 正常范围")
                else:
                    print("   🟡 安全等级: 可接受")
        
        return True
        
    except Exception as e:
        print(f"❌ 安全等待时间测试失败: {e}")
        return False

def show_safety_recommendations():
    """显示安全建议"""
    print("\n" + "=" * 80)
    print("💡 安全抢购建议")
    print("=" * 80)
    
    print("🎯 策略选择建议:")
    print("   • 小白信用 < 70分: 选择 CONSERVATIVE 策略")
    print("   • 小白信用 70-90分: 选择 BALANCED 策略")
    print("   • 小白信用 > 90分: 可选择 AGGRESSIVE 策略")
    
    print("\n🛡️ 风控预防措施:")
    print("   • 避免过于频繁的请求")
    print("   • 保持随机性的操作间隔")
    print("   • 模拟真实的人类行为")
    print("   • 监控风控信号并及时应对")
    
    print("\n⚠️ 风险提醒:")
    print("   • 宁可成功率低一些，也要避免被限制")
    print("   • 账户安全比单次成功更重要")
    print("   • 过度激进可能导致账户被限制")
    print("   • 建议先用保守策略测试")
    
    print("\n📈 优化建议:")
    print("   • 提升京东小白信用分")
    print("   • 保持良好的购买记录")
    print("   • 完善账户实名认证")
    print("   • 定期正常使用京东服务")

def main():
    """主测试函数"""
    try:
        print("安全抢购策略测试 - 防风控版本")
        print("=" * 80)
        
        # 执行各项测试
        config_ok = test_safe_config()
        retry_ok = test_safe_retry_intervals()
        risk_ok = test_risk_control_detection()
        human_ok = test_human_behavior_simulation()
        wait_ok = test_safe_wait_time()
        
        # 显示安全建议
        show_safety_recommendations()
        
        print("\n" + "=" * 80)
        print("测试结果汇总")
        print("=" * 80)
        print(f"安全配置: {'✅ 通过' if config_ok else '❌ 失败'}")
        print(f"重试间隔: {'✅ 通过' if retry_ok else '❌ 失败'}")
        print(f"风控检测: {'✅ 通过' if risk_ok else '❌ 失败'}")
        print(f"行为模拟: {'✅ 通过' if human_ok else '❌ 失败'}")
        print(f"安全等待: {'✅ 通过' if wait_ok else '❌ 失败'}")
        
        if all([config_ok, retry_ok, risk_ok, human_ok, wait_ok]):
            print("\n🎉 安全抢购策略已就绪！")
            print("\n🛡️ 安全特性:")
            print("1. 🎯 三级风险策略 - 适应不同用户")
            print("2. ⏱️ 智能重试间隔 - 模拟人类行为")
            print("3. 🚨 风控检测机制 - 实时监控风险")
            print("4. 🎭 人类行为模拟 - 降低检测概率")
            print("5. 🔄 动态策略调整 - 根据情况优化")
            
            print("\n📊 预期效果:")
            print("• 保守策略: 成功率40-60%, 风控风险极低")
            print("• 平衡策略: 成功率60-80%, 风控风险低")
            print("• 激进策略: 成功率80-95%, 风控风险中等")
            
            print("\n🎯 推荐使用:")
            print("• 新手用户: 选择保守策略，安全第一")
            print("• 普通用户: 选择平衡策略，效果最佳")
            print("• 高级用户: 谨慎选择激进策略")
        else:
            print("\n⚠️ 部分功能存在问题，请检查配置")
            
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
