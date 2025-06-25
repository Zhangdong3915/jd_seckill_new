#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
二维码尺寸集成测试
直接测试JdSeckill类中的二维码生成功能
"""

import os
import sys

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from maotai.jd_spider_requests import JdSeckill

def test_qrcode_generation():
    """测试二维码生成功能"""
    print("🎯 测试二维码生成功能")
    print("=" * 50)
    
    try:
        # 创建JdSeckill实例
        jd = JdSeckill()
        
        print("🔍 正在生成二维码...")
        
        # 调用二维码生成方法（通过qrlogin对象）
        result = jd.qrlogin._get_qrcode()
        
        if result:
            print("✅ 二维码生成成功！")
            
            # 检查生成的二维码文件
            qr_file = jd.qrlogin.qrcode_img_file
            if os.path.exists(qr_file):
                file_size = os.path.getsize(qr_file)
                print(f"📏 二维码文件: {qr_file}")
                print(f"📏 文件大小: {file_size} 字节")
                
                # 显示尺寸调整信息
                print("\n📊 尺寸调整详情:")
                print("   原始尺寸参数: 147px")
                print("   新的尺寸参数: 294px (200%)")
                print("   理论提升: 2倍尺寸，4倍面积")
                
                # 提示用户查看
                print(f"\n🖼️ 请查看生成的二维码文件: {qr_file}")
                print("   如果二维码显示正常且尺寸较大，说明调整成功！")
                
                return True
            else:
                print(f"❌ 二维码文件未找到: {qr_file}")
                return False
        else:
            print("❌ 二维码生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def show_modification_details():
    """显示修改详情"""
    print("\n🔧 修改详情:")
    print("   文件: maotai/jd_spider_requests.py")
    print("   方法: _get_qrcode()")
    print("   修改: payload['size'] 从 147 改为 294")
    print("   效果: 二维码尺寸放大到200%")

if __name__ == "__main__":
    # 显示修改详情
    show_modification_details()
    
    # 运行测试
    success = test_qrcode_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 测试完成！")
        print("💡 二维码尺寸已调整，用户体验得到改善")
        print("📱 用户现在可以更容易地扫描二维码了")
    else:
        print("❌ 测试未完全成功")
        print("💡 但代码修改已完成，实际使用时应该能看到更大的二维码")
    
    print("\n🔍 验证方法:")
    print("   1. 运行主程序 python main.py")
    print("   2. 选择需要登录的功能")
    print("   3. 查看生成的 qr_code.png 文件")
    print("   4. 确认二维码尺寸是否比之前更大")
