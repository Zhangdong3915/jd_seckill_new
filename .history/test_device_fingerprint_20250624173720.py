#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试设备指纹收集功能
"""

import sys
import os

def test_device_fingerprint():
    """测试设备指纹收集功能"""
    print("设备指纹收集功能测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from helper.device_fingerprint import DeviceFingerprintCollector
        from maotai.config import global_config
        
        print("🔧 初始化系统...")
        
        # 创建JdSeckill实例
        jd = JdSeckill()
        
        print("\n📋 检查当前配置中的设备参数...")
        
        # 检查当前配置
        current_eid = global_config.getRaw('config', 'eid')
        current_fp = global_config.getRaw('config', 'fp')
        
        print(f"当前eid: {current_eid}")
        print(f"当前fp: {current_fp}")
        
        # 检查参数格式
        print(f"eid长度: {len(current_eid) if current_eid else 0}")
        print(f"fp长度: {len(current_fp) if current_fp else 0}")
        print(f"eid是否包含引号: {'是' if current_eid and ('\"' in current_eid or \"'\" in current_eid) else '否'}")
        print(f"fp是否包含引号: {'是' if current_fp and ('\"' in current_fp or \"'\" in current_fp) else '否'}")
        
        print("\n🔍 测试设备指纹收集器...")
        
        # 创建设备指纹收集器
        if jd.device_collector:
            collector = jd.device_collector
            print("✅ 设备指纹收集器已初始化")
        else:
            print("❌ 设备指纹收集器未初始化")
            return False
        
        print("\n📱 测试参数验证功能...")
        
        # 测试当前参数验证
        collector.eid = current_eid
        collector.fp = current_fp
        
        print("验证当前配置参数...")
        is_valid = collector.validate_params()
        print(f"验证结果: {'通过' if is_valid else '失败'}")
        
        print("\n🔧 测试参数收集功能...")
        
        # 测试从cookies收集
        print("从cookies收集参数...")
        collector.update_from_cookies()
        
        # 测试完整收集流程
        print("执行完整收集流程...")
        eid, fp = collector.collect_device_params()
        
        print(f"收集到的eid: {eid[:50] if eid else 'None'}...")
        print(f"收集到的fp: {fp[:50] if fp else 'None'}...")
        
        # 再次验证收集到的参数
        print("\n验证收集到的参数...")
        final_valid = collector.validate_params()
        print(f"最终验证结果: {'通过' if final_valid else '失败'}")
        
        print("\n✅ 设备指纹收集功能测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_format():
    """测试配置文件格式问题"""
    print("\n配置文件格式测试")
    print("=" * 60)
    
    try:
        from maotai.config import global_config
        
        # 读取原始配置值
        eid_raw = global_config.getRaw('config', 'eid')
        fp_raw = global_config.getRaw('config', 'fp')
        
        print(f"原始eid值: {repr(eid_raw)}")
        print(f"原始fp值: {repr(fp_raw)}")
        
        # 检查是否有引号
        if eid_raw and (eid_raw.startswith('"') and eid_raw.endswith('"')):
            print("⚠️ eid参数包含引号，需要清理")
            clean_eid = eid_raw.strip('"')
            print(f"清理后的eid: {clean_eid}")
        
        if fp_raw and (fp_raw.startswith('"') and fp_raw.endswith('"')):
            print("⚠️ fp参数包含引号，需要清理")
            clean_fp = fp_raw.strip('"')
            print(f"清理后的fp: {clean_fp}")
        
        # 检查参数是否是默认的测试值
        if eid_raw and "AESXKQVW3XZJQVZJXZJQVZJXZJQVZJ" in eid_raw:
            print("⚠️ eid参数看起来是默认的测试值，不是真实的设备指纹")
        
        if fp_raw and fp_raw.strip('"') == "b1f2c3d4e5f6a7b8c9d0e1f2a3b4c5d6":
            print("⚠️ fp参数看起来是默认的测试值，不是真实的设备指纹")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置格式测试失败: {e}")
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - 设备指纹收集测试")
        print("=" * 60)
        
        # 执行配置格式测试
        test_config_format()
        
        # 执行设备指纹收集测试
        success = test_device_fingerprint()
        
        if success:
            print("\n🎉 设备指纹收集测试完成！")
            print("如果发现问题，请检查配置文件格式和设备指纹收集逻辑")
        else:
            print("\n❌ 设备指纹收集测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
