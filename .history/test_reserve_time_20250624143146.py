#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试预约时间配置读取功能
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from maotai.config import global_config
from maotai.jd_spider_requests import JdSeckill

def test_reserve_time_config():
    """测试预约时间配置读取"""
    print("=" * 60)
    print("🧪 测试预约时间配置读取功能")
    print("=" * 60)
    
    try:
        # 测试直接从配置文件读取
        reserve_time_from_config = global_config.getRaw('config', 'reserve_time') or '10:05:00.000'
        print(f"✅ 从配置文件读取预约时间: {reserve_time_from_config}")
        
        # 测试通过JdSeckill类读取
        jd_seckill = JdSeckill()
        reserve_time_from_class = jd_seckill.get_reserve_time_str()
        print(f"✅ 通过JdSeckill类读取预约时间: {reserve_time_from_class}")
        
        # 验证两种方式读取的结果是否一致
        if reserve_time_from_config == reserve_time_from_class:
            print("✅ 两种读取方式结果一致")
        else:
            print("❌ 两种读取方式结果不一致")
            
        # 测试时间状态获取（不需要登录）
        print("\n📊 测试时间状态获取功能:")
        try:
            time_status = jd_seckill.get_time_status()
            print(f"✅ 当前状态: {time_status['status']}")
            print(f"✅ 状态描述: {time_status['description']}")
            print(f"✅ 下一步操作: {time_status['action']}")
        except Exception as e:
            print(f"⚠️ 时间状态获取测试失败: {e}")
            
        print("\n" + "=" * 60)
        print("🎉 预约时间配置测试完成")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reserve_time_config()
