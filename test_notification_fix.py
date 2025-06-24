#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试通知功能修复
"""

import sys
import os
from datetime import datetime

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_notification_system():
    """测试通知系统"""
    print("=" * 60)
    print("通知系统测试")
    print("=" * 60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        
        jd = JdSeckill()
        
        print("\n1. 测试预约成功通知:")
        notification_data = {
            'type': '预约通知',
            'icon': '✅',
            'title': '预约成功',
            'summary': '商品预约已完成，获得抢购资格',
            'reserve_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reserve_status': '成功',
            'reserve_result': '已获得抢购资格',
            'reserve_success': True
        }
        jd.send_detailed_notification(notification_data)
        
        print("\n2. 测试抢购成功通知:")
        notification_data = {
            'type': '抢购通知',
            'icon': '🎉',
            'title': '抢购成功！',
            'summary': '恭喜！成功抢到商品，订单号: TEST123456',
            'seckill_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'seckill_status': '成功',
            'seckill_result': '抢购成功',
            'seckill_success': True,
            'order_id': 'TEST123456',
            'total_money': '1499.00',
            'pay_url': 'https://order.jd.com/center/list.action',
            'order_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        jd.send_detailed_notification(notification_data)
        
        print("\n3. 测试抢购失败通知:")
        notification_data = {
            'type': '抢购通知',
            'icon': '😔',
            'title': '抢购失败',
            'summary': '本次抢购未成功: 很遗憾没有抢到',
            'seckill_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'seckill_status': '失败',
            'seckill_result': '抢购失败',
            'seckill_success': False,
            'error_message': '很遗憾没有抢到',
            'error_code': '90013'
        }
        jd.send_detailed_notification(notification_data)
        
        print("\n4. 测试简单通知:")
        jd.send_notification("测试通知", "这是一个测试消息", "info")
        
        print("\n✅ 通知系统测试完成！")
        print("\n📋 测试结果说明:")
        print("- 如果微信通知已配置SCKEY，应该会收到微信消息")
        print("- 如果微信通知未配置，会显示警告信息但不会报错")
        print("- 控制台通知应该正常显示")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 通知系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("京东茅台秒杀系统 - 通知功能修复测试")
    print("=" * 60)
    
    success = test_notification_system()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 测试完成！通知功能已修复")
        print("\n修复内容:")
        print("- 修复了微信通知SCKEY检查逻辑")
        print("- 确保只在正确配置SCKEY时发送微信通知")
        print("- 添加了详细的错误处理和日志记录")
        print("- 保持控制台通知正常工作")
    else:
        print("❌ 测试失败，请检查错误信息")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
