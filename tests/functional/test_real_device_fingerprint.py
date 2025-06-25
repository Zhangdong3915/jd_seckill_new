#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试真实设备指纹收集功能
"""

import sys
import os

def test_real_device_fingerprint():
    """测试真实设备指纹收集功能"""
    print("真实设备指纹收集测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from helper.device_fingerprint import DeviceFingerprintCollector
        from maotai.config import global_config
        
        print("🔧 初始化系统...")
        
        # 创建JdSeckill实例
        jd = JdSeckill()
        
        print("\n📋 当前配置状态...")
        current_eid = global_config.getRaw('config', 'eid')
        current_fp = global_config.getRaw('config', 'fp')
        print(f"配置文件中的eid: {current_eid[:30]}...")
        print(f"配置文件中的fp: {current_fp}")
        
        print("\n🔍 测试真实设备指纹收集...")
        
        # 使用已登录的session进行收集
        if jd.device_collector:
            collector = jd.device_collector
            print("✅ 设备指纹收集器已初始化")
            
            # 强制重新收集设备指纹
            print("\n📱 开始从京东页面收集真实设备指纹...")
            eid, fp = collector.collect_device_params()
            
            if eid and fp:
                print(f"\n✅ 收集到真实设备指纹:")
                print(f"   新eid: {eid[:50]}...")
                print(f"   新fp: {fp}")
                
                # 验证新参数
                collector.eid = eid
                collector.fp = fp
                is_valid = collector.validate_params()
                print(f"   验证结果: {'通过' if is_valid else '失败'}")
                
                # 如果验证通过，更新配置文件
                if is_valid:
                    print("\n🔧 更新配置文件...")
                    try:
                        # 更新设备参数
                        jd.update_device_params_and_reload(eid, fp)
                        print("✅ 配置文件已更新")
                        
                        # 验证更新后的配置
                        new_eid = global_config.getRaw('config', 'eid')
                        new_fp = global_config.getRaw('config', 'fp')
                        print(f"   更新后的eid: {new_eid[:50]}...")
                        print(f"   更新后的fp: {new_fp}")
                        
                    except Exception as e:
                        print(f"❌ 配置文件更新失败: {e}")
                
            else:
                print("❌ 未能收集到有效的设备指纹")
                
        else:
            print("❌ 设备指纹收集器未初始化")
            return False
        
        print("\n✅ 真实设备指纹收集测试完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_extraction():
    """测试手动提取设备指纹的方法"""
    print("\n手动设备指纹提取测试")
    print("=" * 60)
    
    try:
        from helper.device_fingerprint import DeviceFingerprintCollector
        import requests
        
        # 创建session
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        collector = DeviceFingerprintCollector(session)
        
        print("🔍 测试从茅台商品页面提取设备指纹...")
        
        # 访问茅台商品页面
        from maotai.config import global_config
        sku_id = global_config.getRaw('config', 'sku_id')
        url = f"https://item.jd.com/{sku_id}.html"
        
        print(f"访问商品页面: {url}")
        
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ 成功访问商品页面")
            
            # 查找JavaScript变量
            html_content = response.text
            
            # 检查是否包含目标变量
            if '_JdEid' in html_content:
                print("✅ 页面包含_JdEid变量")
            else:
                print("⚠️ 页面不包含_JdEid变量")
            
            if '_JdJrTdRiskFpInfo' in html_content:
                print("✅ 页面包含_JdJrTdRiskFpInfo变量")
            else:
                print("⚠️ 页面不包含_JdJrTdRiskFpInfo变量")
            
            # 尝试提取
            collector._extract_params_from_html(html_content)
            
            if collector.eid:
                print(f"✅ 提取到eid: {collector.eid[:50]}...")
            else:
                print("❌ 未能提取到eid")
            
            if collector.fp:
                print(f"✅ 提取到fp: {collector.fp}")
            else:
                print("❌ 未能提取到fp")
                
        else:
            print(f"❌ 访问商品页面失败: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ 手动提取测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    try:
        print("京东茅台秒杀系统 - 真实设备指纹收集测试")
        print("=" * 60)
        
        # 执行真实设备指纹收集测试
        success1 = test_real_device_fingerprint()
        
        # 执行手动提取测试
        success2 = test_manual_extraction()
        
        if success1 and success2:
            print("\n🎉 所有测试完成！")
            print("现在程序应该能够自动获取真实的京东设备指纹参数了")
        else:
            print("\n❌ 部分测试失败")
        
        return success1 and success2
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
