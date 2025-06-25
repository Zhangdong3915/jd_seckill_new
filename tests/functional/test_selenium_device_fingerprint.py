#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Selenium设备指纹收集功能
验证完整的集成方案
"""

import sys
import os

def test_selenium_integration():
    """测试Selenium集成到主系统的功能"""
    print("Selenium设备指纹集成测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from maotai.config import global_config
        
        print("🔧 初始化系统...")
        
        # 创建JdSeckill实例
        jd = JdSeckill()
        
        print("\n📋 当前配置状态...")
        current_eid = global_config.getRaw('config', 'eid')
        current_fp = global_config.getRaw('config', 'fp')
        print(f"配置文件中的eid: {current_eid[:30]}...")
        print(f"配置文件中的fp: {current_fp}")
        
        print("\n🚀 测试集成的Selenium设备指纹收集...")
        
        # 测试设备指纹收集（启用selenium）
        jd._collect_device_fingerprint(use_selenium=True)
        
        print("\n📋 检查更新后的配置...")
        new_eid = global_config.getRaw('config', 'eid')
        new_fp = global_config.getRaw('config', 'fp')
        print(f"更新后的eid: {new_eid[:30]}...")
        print(f"更新后的fp: {new_fp}")
        
        # 检查是否有变化
        if new_eid != current_eid or new_fp != current_fp:
            print("✅ 设备指纹参数已更新")
            
            # 验证新参数
            if jd.device_collector:
                jd.device_collector.eid = new_eid
                jd.device_collector.fp = new_fp
                is_valid = jd.device_collector.validate_params()
                print(f"   新参数验证结果: {'通过' if is_valid else '失败'}")
        else:
            print("⚠️ 设备指纹参数未发生变化")
        
        print("\n✅ Selenium集成测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_selenium_only():
    """测试纯Selenium设备指纹收集"""
    print("\n纯Selenium设备指纹收集测试")
    print("=" * 60)
    
    try:
        from helper.selenium_device_fingerprint import SeleniumDeviceFingerprintCollector
        
        print("🌐 启动Selenium设备指纹收集器...")
        
        # 创建收集器（使用无头模式）
        collector = SeleniumDeviceFingerprintCollector(headless=True, timeout=30)
        
        # 收集设备指纹
        eid, fp = collector.collect_from_jd_pages()
        
        if eid and fp:
            print(f"\n✅ Selenium设备指纹收集成功:")
            print(f"   eid: {eid}")
            print(f"   fp: {fp}")
            
            # 验证设备指纹
            is_valid, message = collector.validate_fingerprint(eid, fp)
            print(f"   验证结果: {'通过' if is_valid else '失败'} - {message}")
            
            return True
        else:
            print("\n❌ Selenium设备指纹收集失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_mechanism():
    """测试回退机制"""
    print("\n回退机制测试")
    print("=" * 60)
    
    try:
        from helper.device_fingerprint import DeviceFingerprintCollector
        import requests
        
        # 创建设备指纹收集器
        session = requests.Session()
        collector = DeviceFingerprintCollector(session)
        
        print("🔍 测试常规方法 + Selenium回退...")
        
        # 测试完整的收集流程
        eid, fp = collector.collect_device_params(use_selenium=True)
        
        if eid and fp:
            print(f"\n✅ 设备指纹收集成功:")
            print(f"   eid: {eid[:50]}...")
            print(f"   fp: {fp}")
            
            # 验证设备指纹
            collector.eid = eid
            collector.fp = fp
            is_valid = collector.validate_params()
            print(f"   验证结果: {'通过' if is_valid else '失败'}")
            
            return True
        else:
            print("\n❌ 设备指纹收集失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_update():
    """测试配置文件更新功能"""
    print("\n配置文件更新测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from maotai.config import global_config
        
        # 创建JdSeckill实例
        jd = JdSeckill()
        
        # 备份当前配置
        backup_eid = global_config.getRaw('config', 'eid')
        backup_fp = global_config.getRaw('config', 'fp')
        
        print(f"备份当前配置:")
        print(f"   eid: {backup_eid[:30]}...")
        print(f"   fp: {backup_fp}")
        
        # 生成测试用的新设备指纹
        test_eid = "TEST_EID_" + "X" * 50
        test_fp = "test_fp_" + "a" * 24
        
        print(f"\n测试更新配置:")
        print(f"   新eid: {test_eid[:30]}...")
        print(f"   新fp: {test_fp}")
        
        # 更新配置
        jd.update_device_params_and_reload(test_eid, test_fp)
        
        # 验证更新
        updated_eid = global_config.getRaw('config', 'eid')
        updated_fp = global_config.getRaw('config', 'fp')
        
        print(f"\n更新后的配置:")
        print(f"   eid: {updated_eid[:30]}...")
        print(f"   fp: {updated_fp}")
        
        # 检查更新是否成功
        if updated_eid == test_eid and updated_fp == test_fp:
            print("✅ 配置更新成功")
            
            # 恢复原配置
            print("\n恢复原配置...")
            jd.update_device_params_and_reload(backup_eid, backup_fp)
            
            # 验证恢复
            restored_eid = global_config.getRaw('config', 'eid')
            restored_fp = global_config.getRaw('config', 'fp')
            
            if restored_eid == backup_eid and restored_fp == backup_fp:
                print("✅ 配置恢复成功")
                return True
            else:
                print("⚠️ 配置恢复失败")
                return False
        else:
            print("❌ 配置更新失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - Selenium设备指纹收集完整测试")
        print("=" * 60)
        
        # 执行所有测试
        tests = [
            ("配置文件更新测试", test_config_update),
            ("纯Selenium收集测试", test_selenium_only),
            ("回退机制测试", test_fallback_mechanism),
            ("系统集成测试", test_selenium_integration),
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_func()
                results.append((test_name, result))
                print(f"{'✅ 通过' if result else '❌ 失败'}: {test_name}")
            except Exception as e:
                print(f"❌ 异常: {test_name} - {e}")
                results.append((test_name, False))
        
        # 总结
        print(f"\n{'='*60}")
        print("测试总结:")
        print("="*60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   {status}: {test_name}")
        
        print(f"\n总计: {passed}/{total} 个测试通过")
        
        if passed == total:
            print("\n🎉 所有测试通过！Selenium设备指纹收集功能已完全集成")
            print("现在程序可以自动获取真实的京东设备指纹参数了")
        else:
            print(f"\n⚠️ {total - passed} 个测试失败，请检查相关功能")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
