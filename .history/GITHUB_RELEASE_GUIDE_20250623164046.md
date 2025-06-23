# GitHub Release 发布指南

本文档说明如何使用GitHub Release来发布京东茅台秒杀系统的新版本。

## 🎯 发布流程概述

1. **代码准备**: 确保所有代码已提交并推送到主分支
2. **创建标签**: 使用发布脚本创建版本标签
3. **自动构建**: GitHub Actions自动构建Windows可执行文件
4. **创建Release**: 自动创建GitHub Release并上传文件
5. **用户下载**: 用户从Release页面下载最新版本

## 📋 准备工作

### 1. 确保代码已提交
```bash
git add .
git commit -m "feat: 准备发布v2.1.1版本"
git push origin main
```

### 2. 检查版本号
确保以下文件中的版本号已更新：
- `README.md`
- `EXE打包工具.py`
- 其他相关文档

## 🚀 发布新版本

### 方法1: 使用发布脚本（推荐）
```bash
python scripts/release.py
```

脚本会：
1. 检查Git状态
2. 获取当前版本号
3. 创建并推送标签
4. 触发GitHub Actions

### 方法2: 手动创建标签
```bash
# 创建标签
git tag -a v2.1.1 -m "Release v2.1.1"

# 推送标签
git push origin v2.1.1
```

## 🔧 GitHub Actions 工作流

当推送标签时，GitHub Actions会自动：

1. **设置环境**: Python 3.11 + 依赖安装
2. **构建程序**: 运行 `EXE打包工具.py`
3. **创建Release**: 使用预定义模板
4. **上传文件**: 将ZIP文件上传到Release

### 工作流文件位置
`.github/workflows/release.yml`

### 构建状态查看
访问: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`

## 📦 Release 内容

每个Release包含：

### 文件
- `京东茅台秒杀系统_vX.X.X_完整版.zip` - Windows可执行程序

### 说明
- 版本特性介绍
- 下载和安装说明
- 使用指南
- 技术改进说明
- 问题修复列表

## 🔗 用户下载流程

用户可以通过以下方式下载：

1. **GitHub Release页面**:
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO/releases
   ```

2. **直接下载链接**:
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v2.1.1/京东茅台秒杀系统_v2.1.1_完整版.zip
   ```

3. **最新版本**:
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO/releases/latest
   ```

## 📊 版本管理策略

### 版本号格式
使用语义化版本号: `vMAJOR.MINOR.PATCH`

- **MAJOR**: 重大功能变更或不兼容更新
- **MINOR**: 新功能添加，向后兼容
- **PATCH**: Bug修复，向后兼容

### 示例
- `v2.1.1` - 修复bug
- `v2.2.0` - 新增功能
- `v3.0.0` - 重大更新

## 🛠️ 故障排除

### 构建失败
1. 检查GitHub Actions日志
2. 确认依赖是否正确安装
3. 检查打包脚本是否有错误

### 标签创建失败
1. 确认标签名称格式正确（v开头）
2. 检查是否有权限推送标签
3. 确认标签不存在冲突

### Release创建失败
1. 检查GitHub Token权限
2. 确认仓库设置允许创建Release
3. 检查工作流文件语法

## 📝 最佳实践

### 发布前检查清单
- [ ] 所有代码已提交并推送
- [ ] 版本号已更新
- [ ] 功能测试通过
- [ ] 文档已更新
- [ ] 无未解决的严重bug

### Release说明编写
- 使用清晰的标题和分类
- 突出重要的新功能和修复
- 提供详细的使用说明
- 包含必要的警告和提醒

### 用户体验
- 提供清晰的下载链接
- 包含完整的安装说明
- 提供技术支持信息
- 维护版本历史记录

## 🔄 自动化改进

### 未来可以添加的功能
1. **自动版本号递增**
2. **变更日志自动生成**
3. **多平台构建支持**
4. **自动化测试集成**
5. **下载统计和分析**

## 📞 技术支持

如果在发布过程中遇到问题：

1. 查看GitHub Actions日志
2. 检查工作流配置
3. 确认仓库权限设置
4. 联系项目维护者

---

通过这套GitHub Release流程，您可以：
- ✅ 避免在代码仓库中存储大文件
- ✅ 提供专业的版本管理
- ✅ 自动化构建和发布流程
- ✅ 为用户提供便捷的下载体验
