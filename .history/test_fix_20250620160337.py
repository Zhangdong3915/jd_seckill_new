#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的程序是否能正常启动
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有模块是否能正常导入"""
    try:
        from maotai.jd_spider_requests import JdSeckill
        from maotai.timer import Timer
        from maotai.config import global_config
        from error.exception import SKException
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_config():
    """测试配置文件读取"""
    try:
        from maotai.config import global_config
        sku_id = global_config.getRaw('config', 'sku_id')
        buy_time = global_config.getRaw('config', 'buy_time')
        print(f"✅ 配置读取成功 - 商品ID: {sku_id}, 购买时间: {buy_time}")
        return True
    except Exception as e:
        print(f"❌ 配置读取失败: {e}")
        return False

def test_timer():
    """测试Timer类初始化"""
    try:
        from maotai.timer import Timer
        timer = Timer()
        print(f"✅ Timer初始化成功 - 购买时间: {timer.buy_time}")
        print(f"✅ 时间差: {timer.diff_time}ms")
        return True
    except Exception as e:
        print(f"❌ Timer初始化失败: {e}")
        return False

def test_jd_seckill():
    """测试JdSeckill类初始化"""
    try:
        from maotai.jd_spider_requests import JdSeckill
        jd = JdSeckill()
        print(f"✅ JdSeckill初始化成功 - 商品ID: {jd.sku_id}")
        return True
    except Exception as e:
        print(f"❌ JdSeckill初始化失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("京东秒杀项目修复测试")
    print("=" * 50)
    
    tests = [
        ("模块导入测试", test_imports),
        ("配置文件测试", test_config),
        ("Timer类测试", test_timer),
        ("JdSeckill类测试", test_jd_seckill),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   测试失败，请检查相关代码")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！程序修复成功！")
        print("\n📝 使用说明:")
        print("1. 运行 python main.py 启动程序")
        print("2. 选择功能: 1-预约商品, 2-秒杀抢购")
        print("3. 首次使用需要扫码登录京东账号")
        print("4. 确保config.ini中的参数配置正确")
    else:
        print("❌ 部分测试失败，请检查错误信息")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
