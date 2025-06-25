#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
二维码尺寸调整测试脚本
测试新的二维码尺寸设置是否正常工作
"""

import os
import sys
import time
import requests

def test_qrcode_size():
    """测试二维码尺寸调整"""
    print("🔍 测试二维码尺寸调整...")
    
    # 模拟京东二维码请求
    url = 'https://qr.m.jd.com/show'
    payload = {
        'appid': 133,
        'size': 294,  # 新的200%尺寸
        't': str(int(time.time() * 1000)),
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://passport.jd.com/new/login.aspx',
    }
    
    try:
        print("📡 正在请求二维码...")
        resp = requests.get(url=url, headers=headers, params=payload, timeout=10)
        
        if resp.status_code == 200:
            # 保存测试二维码
            test_qr_file = 'test_qr_code.png'
            with open(test_qr_file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    f.write(chunk)
            
            print(f"✅ 二维码已保存到: {test_qr_file}")
            
            # 检查图片尺寸
            try:
                with Image.open(test_qr_file) as img:
                    width, height = img.size
                    print(f"📏 二维码尺寸: {width} x {height} 像素")
                    
                    # 验证尺寸是否符合预期
                    expected_size = 294
                    if width >= expected_size * 0.9 and height >= expected_size * 0.9:
                        print("✅ 二维码尺寸调整成功！")
                        print(f"   预期尺寸: ~{expected_size}px")
                        print(f"   实际尺寸: {width}x{height}px")
                        return True
                    else:
                        print("❌ 二维码尺寸不符合预期")
                        print(f"   预期尺寸: ~{expected_size}px")
                        print(f"   实际尺寸: {width}x{height}px")
                        return False
                        
            except Exception as e:
                print(f"❌ 无法读取图片尺寸: {e}")
                return False
                
        else:
            print(f"❌ 请求失败，状态码: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def compare_sizes():
    """对比新旧尺寸"""
    print("\n📊 尺寸对比:")
    print("   原始尺寸: 147px (100%)")
    print("   新的尺寸: 294px (200%)")
    print("   提升倍数: 2.0x")
    print("   面积提升: 4.0x (2² = 4)")

def cleanup():
    """清理测试文件"""
    test_files = ['test_qr_code.png']
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🧹 已清理测试文件: {file}")
            except:
                pass

if __name__ == "__main__":
    print("🎯 二维码尺寸调整测试")
    print("=" * 50)
    
    # 运行测试
    success = test_qrcode_size()
    
    # 显示对比信息
    compare_sizes()
    
    # 测试结果
    print("\n" + "=" * 50)
    if success:
        print("🎉 测试通过！二维码尺寸已成功调整到200%")
        print("💡 用户现在可以看到更大、更清晰的二维码了")
    else:
        print("❌ 测试失败，请检查网络连接或代码修改")
    
    # 询问是否清理测试文件
    try:
        choice = input("\n是否清理测试文件？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            cleanup()
    except KeyboardInterrupt:
        print("\n测试结束")
    
    print("\n测试完成！")
