# 测试文件目录说明

## 目录结构

```
tests/
├── functional/     # 功能测试 - 完整功能的端到端测试
├── integration/    # 集成测试 - 系统组件间的集成测试
├── unit/          # 单元测试 - 单个模块的测试
└── archive/       # 归档文件 - 临时或过时的测试文件
```

## 各目录说明

### functional/ - 功能测试
完整功能的端到端测试，验证系统主要功能是否正常工作。

**包含文件**:
- 登录流程测试
- 设备指纹收集测试
- 通知系统测试
- Selenium集成测试

### integration/ - 集成测试
验证不同系统组件之间的协作是否正常。

**包含文件**:
- 配置系统集成测试
- 安全组件集成测试
- 消息通知集成测试

### unit/ - 单元测试
针对单个模块或函数的测试。

**包含文件**:
- 工具函数测试
- 配置解析测试
- 时间同步测试

### archive/ - 归档文件
临时调试文件、过时的测试文件或实验性代码。

**包含文件**:
- 调试用的临时测试
- 已废弃的测试方法
- 实验性功能测试

## 运行测试

### 运行所有功能测试
```bash
cd tests/functional
python test_*.py
```

### 运行特定测试
```bash
python tests/functional/test_selenium_device_fingerprint.py
```

### 运行集成测试
```bash
cd tests/integration
python test_*.py
```

## 测试文件命名规范

- `test_` 开头
- 使用下划线分隔单词
- 描述性的文件名
- 例如: `test_login_notification.py`

## 注意事项

1. 所有测试文件都应该能够独立运行
2. 测试前确保系统配置正确
3. 某些测试需要网络连接
4. Selenium测试需要Chrome浏览器

## 维护说明

- 新增测试文件请放入对应目录
- 定期清理archive目录中的过时文件
- 更新此README文件以反映最新的测试结构
