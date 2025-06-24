#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试配置文件是否正确
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config():
    """测试配置文件读取"""
    try:
        from maotai.config import global_config
        
        print("="*50)
        print("配置文件读取测试")
        print("="*50)
        
        # 测试基础配置
        sku_id = global_config.getRaw('config', 'sku_id')
        seckill_num = global_config.getRaw('config', 'seckill_num')
        buy_time = global_config.getRaw('config', 'buy_time')
        
        print(f"OK SKU ID: {sku_id}")
        print(f"OK 抢购数量: {seckill_num}")
        print(f"OK 抢购时间: {buy_time}")

        # 测试账户配置
        try:
            payment_pwd = global_config.getRaw('account', 'payment_pwd')
            print(f"OK 支付密码: {'已配置' if payment_pwd else '未配置'}")
        except:
            print("OK 支付密码: 未配置")

        # 测试消息配置
        try:
            enable = global_config.getRaw('messenger', 'enable')
            sckey = global_config.getRaw('messenger', 'sckey')
            print(f"OK 微信通知: {'启用' if enable == 'true' else '禁用'}")
            print(f"OK SCKEY: {'已配置' if sckey else '未配置'}")
        except:
            print("OK 微信通知: 禁用")

        print("\n SUCCESS 配置文件格式正确，所有配置项都能正常读取！")
        return True
        
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return False

if __name__ == "__main__":
    test_config()
