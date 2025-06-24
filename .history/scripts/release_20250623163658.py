#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GitHub Release发布脚本
自动创建标签并触发GitHub Actions构建
"""

import os
import sys
import subprocess
import re
from datetime import datetime

def get_current_version():
    """从代码中获取当前版本号"""
    try:
        # 从README.md中提取版本号
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找版本号模式
        version_pattern = r'v(\d+\.\d+\.\d+)'
        matches = re.findall(version_pattern, content)
        
        if matches:
            return f"v{matches[0]}"
        else:
            return "v2.1.1"  # 默认版本
            
    except Exception as e:
        print(f"获取版本号失败: {e}")
        return "v2.1.1"

def validate_version(version):
    """验证版本号格式"""
    pattern = r'^v\d+\.\d+\.\d+$'
    return re.match(pattern, version) is not None

def check_git_status():
    """检查Git状态"""
    try:
        # 检查是否有未提交的更改
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("⚠️ 检测到未提交的更改:")
            print(result.stdout)
            return False
            
        # 检查是否在主分支
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        current_branch = result.stdout.strip()
        
        if current_branch not in ['main', 'master']:
            print(f"⚠️ 当前分支: {current_branch}")
            print("建议在main或master分支上发布版本")
            
        return True
        
    except Exception as e:
        print(f"检查Git状态失败: {e}")
        return False

def create_tag_and_push(version):
    """创建标签并推送"""
    try:
        # 创建标签
        tag_message = f"Release {version}\n\n自动发布 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        result = subprocess.run(['git', 'tag', '-a', version, '-m', tag_message], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"创建标签失败: {result.stderr}")
            return False
            
        # 推送标签
        result = subprocess.run(['git', 'push', 'origin', version], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"推送标签失败: {result.stderr}")
            return False
            
        print(f"✅ 标签 {version} 创建并推送成功")
        return True
        
    except Exception as e:
        print(f"创建标签失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 GitHub Release 发布工具")
    print("=" * 60)
    
    # 检查是否在项目根目录
    if not os.path.exists('main.py'):
        print("❌ 请在项目根目录下运行此脚本")
        return False
    
    # 检查Git状态
    print("📋 检查Git状态...")
    if not check_git_status():
        response = input("是否继续? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # 获取版本号
    current_version = get_current_version()
    print(f"📦 当前版本: {current_version}")
    
    # 询问版本号
    print("\n请选择操作:")
    print("1. 使用当前版本号发布")
    print("2. 输入新版本号")
    print("3. 取消")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == '1':
        version = current_version
    elif choice == '2':
        version = input("请输入新版本号 (格式: v2.1.2): ").strip()
        if not validate_version(version):
            print("❌ 版本号格式错误，应为 vX.Y.Z 格式")
            return False
    else:
        print("取消发布")
        return False
    
    # 确认发布
    print(f"\n📋 发布信息:")
    print(f"版本号: {version}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n发布流程:")
    print("1. 创建Git标签")
    print("2. 推送到GitHub")
    print("3. 触发GitHub Actions自动构建")
    print("4. 创建GitHub Release")
    print("5. 上传构建的ZIP文件")
    
    confirm = input(f"\n确认发布 {version}? (y/N): ")
    if confirm.lower() != 'y':
        print("取消发布")
        return False
    
    # 创建标签并推送
    print(f"\n🏷️ 创建标签 {version}...")
    if not create_tag_and_push(version):
        return False
    
    print("\n" + "=" * 60)
    print("🎉 发布流程已启动！")
    print("=" * 60)
    print("📋 后续步骤:")
    print("1. GitHub Actions 正在自动构建...")
    print("2. 构建完成后会自动创建 Release")
    print("3. 请访问 GitHub 仓库查看发布状态")
    print("\n🔗 GitHub Actions: https://github.com/YOUR_USERNAME/YOUR_REPO/actions")
    print("🔗 Releases: https://github.com/YOUR_USERNAME/YOUR_REPO/releases")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发布过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
