#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试时间同步功能
"""

import sys
import os
import time
from datetime import datetime

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_time_sources():
    """测试各个时间源"""
    from maotai.timer import Timer
    
    print("=" * 60)
    print("时间同步测试")
    print("=" * 60)
    
    # 创建Timer实例
    timer = Timer()
    
    print(f"本地时间: {datetime.now()}")
    print(f"本地时间戳(ms): {timer.local_time()}")
    
    # 测试各个时间源
    print("\n测试各个时间源:")
    print("-" * 40)
    
    # 测试京东页面时间
    try:
        jd_time = timer._get_jd_time_from_page()
        if jd_time:
            jd_dt = datetime.fromtimestamp(jd_time / 1000)
            print(f"[OK] 京东页面时间: {jd_dt} ({jd_time}ms)")
        else:
            print("[FAIL] 京东页面时间获取失败")
    except Exception as e:
        print(f"[ERROR] 京东页面时间: {e}")
    
    # 测试世界时钟API
    try:
        world_time = timer._get_time_from_worldclock()
        if world_time:
            world_dt = datetime.fromtimestamp(world_time / 1000)
            print(f"[OK] 世界时钟API: {world_dt} ({world_time}ms)")
        else:
            print("[FAIL] 世界时钟API获取失败")
    except Exception as e:
        print(f"[ERROR] 世界时钟API: {e}")
    
    # 测试淘宝时间API
    try:
        tb_time = timer._get_time_from_beijing_time()
        if tb_time:
            tb_dt = datetime.fromtimestamp(tb_time / 1000)
            print(f"[OK] 淘宝时间API: {tb_dt} ({tb_time}ms)")
        else:
            print("[FAIL] 淘宝时间API获取失败")
    except Exception as e:
        print(f"[ERROR] 淘宝时间API: {e}")
    
    # 显示最终使用的时间
    print("\n最终时间同步结果:")
    print("-" * 40)
    final_time = timer.jd_time()
    final_dt = datetime.fromtimestamp(final_time / 1000)
    print(f"网络时间: {final_dt} ({final_time}ms)")
    print(f"本地时间: {datetime.now()} ({timer.local_time()}ms)")
    print(f"时间差: {timer.diff_time}ms")
    
    # 分析时间差
    if abs(timer.diff_time) < 1000:
        print("[OK] 时间同步良好，误差小于1秒")
    elif abs(timer.diff_time) < 5000:
        print("[WARNING] 时间误差较大，建议检查网络")
    else:
        print("[ERROR] 时间误差过大，可能影响抢购精度")

def test_timer_precision():
    """测试定时器精度"""
    from maotai.timer import Timer
    
    print("\n" + "=" * 60)
    print("定时器精度测试")
    print("=" * 60)
    
    timer = Timer()
    
    # 测试时间计算精度
    buy_time_ms = timer.buy_time_ms
    current_time = timer.local_time() - timer.diff_time
    
    time_diff = buy_time_ms - current_time
    
    print(f"设定购买时间: {timer.buy_time}")
    print(f"购买时间戳(ms): {buy_time_ms}")
    print(f"当前网络时间戳(ms): {current_time}")
    print(f"距离购买时间: {time_diff}ms ({time_diff/1000:.1f}秒)")
    
    if time_diff > 0:
        hours = time_diff // (1000 * 60 * 60)
        minutes = (time_diff % (1000 * 60 * 60)) // (1000 * 60)
        seconds = (time_diff % (1000 * 60)) // 1000
        print(f"剩余时间: {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")
    else:
        print("[WARNING] 购买时间已过")

def main():
    """主测试函数"""
    try:
        test_time_sources()
        test_timer_precision()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] 时间同步测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
