#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试增强的通知系统
"""

import sys
import os
import time

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_reserve_notification():
    """测试预约通知"""
    print("="*60)
    print("测试预约通知")
    print("="*60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from datetime import datetime
        
        jd = JdSeckill()
        
        # 测试预约成功通知
        print("\n1. 测试预约成功通知:")
        notification_data = {
            'type': '预约通知',
            'title': '预约成功',
            'summary': '商品预约已完成，获得抢购资格',
            'reserve_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reserve_status': '成功',
            'reserve_result': '已获得抢购资格',
            'reserve_success': True
        }
        jd.send_detailed_notification(notification_data)
        
        time.sleep(2)
        
        # 测试预约失败通知
        print("\n2. 测试预约失败通知:")
        notification_data = {
            'type': '预约通知',
            'title': '预约失败',
            'summary': '预约执行失败，系统将自动重试',
            'reserve_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reserve_status': '失败',
            'reserve_result': '预约未成功',
            'reserve_success': False,
            'error_message': '网络连接超时'
        }
        jd.send_detailed_notification(notification_data)
        
        return True
        
    except Exception as e:
        print(f"预约通知测试失败: {e}")
        return False

def test_seckill_notification():
    """测试抢购通知"""
    print("\n" + "="*60)
    print("测试抢购通知")
    print("="*60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from datetime import datetime
        
        jd = JdSeckill()
        
        # 测试抢购成功通知
        print("\n1. 测试抢购成功通知:")
        notification_data = {
            'type': '抢购通知',
            'title': '抢购成功！',
            'summary': '恭喜！成功抢到商品，订单号: 820227123456',
            'seckill_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'seckill_status': '成功',
            'seckill_result': '抢购成功',
            'seckill_success': True,
            'order_id': '820227123456',
            'total_money': '1499.00',
            'pay_url': 'https://trade.jd.com/shopping/order/getOrderInfo.action?rid=123456',
            'order_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        jd.send_detailed_notification(notification_data)
        
        time.sleep(2)
        
        # 测试抢购失败通知
        print("\n2. 测试抢购失败通知:")
        notification_data = {
            'type': '抢购通知',
            'icon': '😔',
            'title': '抢购失败',
            'summary': '本次抢购未成功: 很遗憾没有抢到，再接再厉哦',
            'seckill_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'seckill_status': '失败',
            'seckill_result': '抢购失败',
            'seckill_success': False,
            'error_message': '很遗憾没有抢到，再接再厉哦',
            'error_code': '60074'
        }
        jd.send_detailed_notification(notification_data)
        
        return True
        
    except Exception as e:
        print(f"抢购通知测试失败: {e}")
        return False

def test_login_notification():
    """测试登录通知"""
    print("\n" + "="*60)
    print("测试登录通知")
    print("="*60)
    
    try:
        from maotai.jd_spider_requests import JdSeckill
        from datetime import datetime
        
        jd = JdSeckill()
        
        # 测试登录成功通知
        print("\n1. 测试登录成功通知:")
        notification_data = {
            'type': '登录通知',
            'icon': '✅',
            'title': '登录成功',
            'summary': '用户 test_user 已成功登录',
            'login_action': '用户登录',
            'login_status': '已登录',
            'login_success': True
        }
        jd.send_detailed_notification(notification_data)
        
        time.sleep(2)
        
        # 测试登录失效通知
        print("\n2. 测试登录失效通知:")
        notification_data = {
            'type': '登录通知',
            'icon': '⚠️',
            'title': '需要重新登录',
            'summary': '检测到登录状态已失效，需要重新登录',
            'login_action': '登录失效',
            'login_status': '未登录',
            'login_success': False,
            'logout_reason': '登录状态过期'
        }
        jd.send_detailed_notification(notification_data)
        
        return True
        
    except Exception as e:
        print(f"登录通知测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("京东茅台秒杀系统 - 增强通知系统测试")
    print("版本: v2.1.1 (2025-06-23)")
    print("测试时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    test_results = []
    
    # 执行各项测试
    test_results.append(("预约通知", test_reserve_notification()))
    test_results.append(("抢购通知", test_seckill_notification()))
    test_results.append(("登录通知", test_login_notification()))
    
    # 输出测试结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("所有通知功能测试通过！")
    else:
        print("部分功能可能需要进一步检查。")
    
    print("\n" + "="*60)
    print("新增功能:")
    print("- 详细的markdown格式通知消息")
    print("- 预约时间、账号、成功状态详情")
    print("- 抢购时间、账号、成功状态、付款链接")
    print("- 登录状态变更通知")
    print("- 支持多账号场景")
    print("="*60)

if __name__ == "__main__":
    main()
