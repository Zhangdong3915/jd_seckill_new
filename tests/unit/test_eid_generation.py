#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试eid生成
"""

from helper.device_fingerprint import DeviceFingerprintCollector
import requests

# 创建一个session
session = requests.Session()
collector = DeviceFingerprintCollector(session)

# 生成eid
eid = collector._generate_eid()
fp = collector._generate_fp()

print(f"生成的eid: {eid}")
print(f"eid长度: {len(eid)}")
print(f"生成的fp: {fp}")
print(f"fp长度: {len(fp)}")

# 测试验证
collector.eid = eid
collector.fp = fp
result = collector.validate_params()
print(f"验证结果: {result}")
