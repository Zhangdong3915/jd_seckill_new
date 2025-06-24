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

# 设置UTF-8编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Windows系统编码处理
if sys.platform.startswith('win'):
    try:
        # 设置控制台代码页为UTF-8
        os.system('chcp 65001 > nul 2>&1')

        # 重新配置标准输出流为UTF-8
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass

def get_latest_tag():
    """获取最新的Git标签"""
    try:
        result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None

    except Exception as e:
        print(f"获取最新标签失败: {e}")
        return None

def get_all_tags():
    """获取所有Git标签"""
    try:
        result = subprocess.run(['git', 'tag', '-l'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            tags = result.stdout.strip().split('\n')
            # 过滤出版本标签并排序
            version_tags = [tag for tag in tags if re.match(r'^v\d+\.\d+\.\d+$', tag)]
            return sorted(version_tags, key=lambda x: [int(i) for i in x[1:].split('.')])
        else:
            return []

    except Exception as e:
        print(f"获取标签列表失败: {e}")
        return []

def suggest_next_version():
    """建议下一个版本号"""
    latest_tag = get_latest_tag()

    if not latest_tag:
        return "v2.1.1"  # 如果没有标签，建议初始版本

    # 解析版本号
    match = re.match(r'^v(\d+)\.(\d+)\.(\d+)$', latest_tag)
    if not match:
        return "v2.1.1"

    major, minor, patch = map(int, match.groups())

    # 建议版本号选项
    suggestions = {
        'patch': f"v{major}.{minor}.{patch + 1}",
        'minor': f"v{major}.{minor + 1}.0",
        'major': f"v{major + 1}.0.0"
    }

    return suggestions

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
    
    # 获取版本信息
    latest_tag = get_latest_tag()
    all_tags = get_all_tags()

    print(f"📦 Git标签信息:")
    if latest_tag:
        print(f"   最新标签: {latest_tag}")
    else:
        print("   最新标签: 无")

    if all_tags:
        print(f"   历史标签: {', '.join(all_tags[-3:])}")  # 显示最近3个标签
    else:
        print("   历史标签: 无")

    # 建议版本号
    suggestions = suggest_next_version()
    if isinstance(suggestions, dict):
        print(f"\n💡 建议的版本号:")
        print(f"   补丁版本 (bug修复): {suggestions['patch']}")
        print(f"   次要版本 (新功能): {suggestions['minor']}")
        print(f"   主要版本 (重大更新): {suggestions['major']}")

    # 询问版本号
    print("\n请选择操作:")
    if isinstance(suggestions, dict):
        print(f"1. 补丁版本 ({suggestions['patch']}) - 推荐用于bug修复")
        print(f"2. 次要版本 ({suggestions['minor']}) - 推荐用于新功能")
        print(f"3. 主要版本 ({suggestions['major']}) - 推荐用于重大更新")
        print("4. 输入自定义版本号")
        print("5. 取消")

        choice = input("请选择 (1-5): ").strip()

        if choice == '1':
            version = suggestions['patch']
        elif choice == '2':
            version = suggestions['minor']
        elif choice == '3':
            version = suggestions['major']
        elif choice == '4':
            version = input("请输入版本号 (格式: v2.1.2): ").strip()
            if not validate_version(version):
                print("❌ 版本号格式错误，应为 vX.Y.Z 格式")
                return False
        else:
            print("取消发布")
            return False
    else:
        print("1. 输入版本号")
        print("2. 取消")

        choice = input("请选择 (1-2): ").strip()

        if choice == '1':
            version = input("请输入版本号 (格式: v2.1.2): ").strip()
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
