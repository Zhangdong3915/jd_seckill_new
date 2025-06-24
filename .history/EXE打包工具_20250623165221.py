#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows EXE打包脚本
使用PyInstaller将项目打包成可执行文件
"""

import os
import sys
import shutil
import zipfile
import subprocess
import re
from datetime import datetime

def get_version_from_git():
    """从Git标签获取版本号"""
    try:
        # 首先尝试获取当前标签
        result = subprocess.run(['git', 'describe', '--exact-match', '--tags'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"检测到Git标签: {version}")
            return version

        # 如果没有当前标签，获取最新标签
        result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"使用最新Git标签: {version}")
            return version

        # 如果没有任何标签，使用默认版本
        print("未找到Git标签，使用默认版本")
        return "v2.1.1"

    except Exception as e:
        print(f"获取Git版本号失败: {e}")
        return "v2.1.1"

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("PyInstaller已安装")
        return True
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller安装成功")
            return True
        except subprocess.CalledProcessError:
            print("PyInstaller安装失败")
            return False

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.ini', '.'),
        ('cookies', 'cookies'),
        ('maotai', 'maotai'),
        ('helper', 'helper'),
        ('README.md', '.'),
        ('bug修复.md', '.'),
        ('京东风控机制分析与安全策略.md', '.'),
        ('极高概率抢购方案.md', '.'),
    ],
    hiddenimports=[
        'requests',
        'configparser',
        'concurrent.futures',
        'datetime',
        'json',
        'time',
        'random',
        'os',
        'sys',
        'logging',
        'psutil',
        'subprocess',
        'PIL',
        'Pillow',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='京东茅台秒杀系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='京东茅台秒杀系统',
)
'''
    
    with open('jd_seckill.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("PyInstaller配置文件已创建")

def build_exe():
    """构建EXE文件"""
    print("开始构建EXE文件...")

    try:
        # 使用spec文件构建
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "jd_seckill.spec"]

        print("正在构建，请稍候...")

        # 方法1：尝试直接运行，不捕获输出以避免编码问题
        try:
            result = subprocess.run(cmd, check=True, timeout=180)
            print("EXE文件构建成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"EXE文件构建失败，返回码: {e.returncode}")

            # 方法2：如果失败，尝试捕获输出但使用更安全的编码
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'  # 替换无法解码的字符
                )
                if result.stderr:
                    print("错误信息:", result.stderr[:500])  # 只显示前500字符
            except:
                pass
            return False
        except subprocess.TimeoutExpired:
            print("构建超时，但可能仍在进行中...")
            # 检查是否生成了文件
            if os.path.exists("dist/京东茅台秒杀系统"):
                print("检测到构建目录，认为构建成功")
                return True
            return False

    except Exception as e:
        print(f"构建过程中出现错误: {e}")
        return False

def create_distribution_package():
    """创建分发包"""
    print("创建分发包...")

    dist_dir = "dist/京东茅台秒杀系统"
    if not os.path.exists(dist_dir):
        print("构建目录不存在")
        return False
    
    # 创建发布目录
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 复制构建结果
    target_dir = os.path.join(release_dir, "京东茅台秒杀系统")
    shutil.copytree(dist_dir, target_dir)
    
    # 复制额外文件
    extra_files = [
        "README.md",
        "bug修复.md", 
        "京东风控机制分析与安全策略.md",
        "极高概率抢购方案.md",
        "config.ini"
    ]
    
    for file in extra_files:
        if os.path.exists(file):
            shutil.copy2(file, target_dir)
    
    # 创建使用说明
    create_usage_guide(target_dir)
    
    print("分发包创建完成")
    return True

def create_usage_guide(target_dir):
    """创建使用说明文件"""
    version = get_version_from_git()
    usage_content = f"""# 京东茅台秒杀系统 - 使用说明

## 🚀 快速开始

### 1. 配置设置
1. 编辑 `config.ini` 文件
2. 填写必要的配置项：
   - sku_id: 商品ID
   - eid 和 fp: 京东风控参数
   - buy_time: 抢购时间
   - risk_level: 安全策略等级

### 2. 运行程序
双击 `京东茅台秒杀系统.exe` 启动程序

### 3. 选择功能
- 1: 预约商品
- 2: 秒杀抢购商品  
- 3: 全自动化执行（推荐）

### 4. 扫码登录
使用京东APP扫描弹出的二维码完成登录

## 🛡️ 安全策略选择

根据您的京东小白信用分选择：
- 小白信用 < 70分: CONSERVATIVE (保守策略)
- 小白信用 70-90分: BALANCED (平衡策略，推荐)
- 小白信用 > 90分: AGGRESSIVE (激进策略)

## ⚠️ 重要提醒

1. 首次使用建议选择保守策略测试
2. 账户安全比单次成功更重要
3. 如遇到验证码或限制，请降低风险等级
4. 详细说明请查看 README.md 文件

## 📞 技术支持

如遇问题请查看：
- README.md - 完整使用说明
- bug修复.md - 常见问题解决方案
- 京东风控机制分析与安全策略.md - 安全策略详解

---
版本: v2.1.1
构建时间: {build_time}
""".format(build_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    with open(os.path.join(target_dir, "使用说明.txt"), 'w', encoding='utf-8') as f:
        f.write(usage_content)

def create_zip_package():
    """创建ZIP压缩包"""
    print("创建ZIP压缩包...")

    release_dir = "release"
    if not os.path.exists(release_dir):
        print("发布目录不存在")
        return False
    
    # 创建ZIP文件名
    version = get_version_from_git()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"京东茅台秒杀系统_{version}_完整版_{timestamp}.zip"
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(release_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, release_dir)
                    zipf.write(file_path, arc_path)
        
        # 获取文件大小
        file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB

        print(f"ZIP压缩包创建成功: {zip_filename}")
        print(f"文件大小: {file_size:.1f} MB")

        return True
    except Exception as e:
        print(f"创建ZIP压缩包失败: {e}")
        return False

def cleanup():
    """清理临时文件"""
    print("清理临时文件...")

    cleanup_items = [
        "build",
        "dist",
        "jd_seckill.spec",
        "__pycache__",
        "release"
    ]

    for item in cleanup_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)

    print("临时文件清理完成")

def main():
    """主函数"""
    print("=" * 60)
    print("京东茅台秒杀系统 - Windows EXE打包工具")
    print("=" * 60)

    # 检查当前目录
    if not os.path.exists("main.py"):
        print("请在项目根目录下运行此脚本")
        return False
    
    # 步骤1: 检查PyInstaller
    if not check_pyinstaller():
        return False
    
    # 步骤2: 创建配置文件
    create_spec_file()
    
    # 步骤3: 构建EXE
    if not build_exe():
        return False
    
    # 步骤4: 创建分发包
    if not create_distribution_package():
        return False
    
    # 步骤5: 创建ZIP压缩包
    if not create_zip_package():
        return False
    
    # 步骤6: 清理临时文件
    cleanup()
    
    print("\n" + "=" * 60)
    print("打包完成！")
    print("=" * 60)
    print("可执行文件已打包成ZIP格式")
    print("ZIP文件包含完整的运行环境")
    print("可直接发送给其他人使用")
    print("\n使用方法:")
    print("1. 解压ZIP文件")
    print("2. 编辑 config.ini 配置文件")
    print("3. 双击 京东茅台秒杀系统.exe 运行")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n打包完成，程序自动退出")
        else:
            print("\n打包失败，程序自动退出")
    except KeyboardInterrupt:
        print("\n\n用户取消操作")
    except Exception as e:
        print(f"\n打包过程中出现未知错误: {e}")
        import traceback
        traceback.print_exc()
