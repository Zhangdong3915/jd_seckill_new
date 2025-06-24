#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安全配置管理模块
处理敏感信息的加密存储和环境变量读取
"""

import os
import base64
import getpass
import configparser
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureConfigManager:
    """安全配置管理器"""
    
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        # 生成加密密钥
        self._init_encryption()
    
    def _init_encryption(self):
        """初始化加密密钥"""
        # 使用机器特征生成固定密钥
        machine_id = self._get_machine_id()
        password = machine_id.encode()
        
        # 使用固定盐值确保密钥一致性
        salt = b'jd_seckill_salt_2025'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher = Fernet(key)
    
    def _get_machine_id(self):
        """获取机器标识"""
        try:
            # Windows
            if os.name == 'nt':
                import subprocess
                result = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line.strip() and 'UUID' not in line:
                            return line.strip()
            
            # Linux/Mac
            else:
                if os.path.exists('/etc/machine-id'):
                    with open('/etc/machine-id', 'r') as f:
                        return f.read().strip()
                elif os.path.exists('/var/lib/dbus/machine-id'):
                    with open('/var/lib/dbus/machine-id', 'r') as f:
                        return f.read().strip()
        except:
            pass
        
        # 备用方案：使用用户名和主机名
        import socket
        return f"{os.getenv('USERNAME', 'user')}_{socket.gethostname()}"
    
    def encrypt_value(self, value):
        """加密值"""
        if not value:
            return ""
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt_value(self, encrypted_value):
        """解密值"""
        if not encrypted_value:
            return ""
        try:
            return self.cipher.decrypt(encrypted_value.encode()).decode()
        except:
            # 如果解密失败，可能是明文，直接返回
            return encrypted_value
    
    def get_secure_value(self, section, key, env_var_name=None, prompt_text=None, allow_input=True):
        """
        获取安全值
        优先级：环境变量 > 配置文件加密值 > 用户输入
        """
        # 1. 尝试从环境变量获取
        if env_var_name:
            env_value = os.getenv(env_var_name)
            if env_value:
                print(f"✅ 从环境变量 {env_var_name} 获取 {key}")
                return env_value
        
        # 2. 尝试从配置文件获取并解密
        try:
            if self.config.has_option(section, key):
                encrypted_value = self.config.get(section, key)
                # 检查是否为空字符串或只包含引号
                if encrypted_value and encrypted_value.strip() and encrypted_value.strip() not in ['""', "''"]:
                    # 如果是明文（没有加密），直接返回
                    if not encrypted_value.startswith('gAAAAA'):  # Fernet加密的特征
                        print(f"✅ 从配置文件获取 {key}")
                        return encrypted_value.strip('"\'')  # 去除引号
                    else:
                        # 尝试解密
                        decrypted_value = self.decrypt_value(encrypted_value)
                        if decrypted_value:
                            print(f"✅ 从配置文件获取 {key}")
                            return decrypted_value
        except:
            pass
        
        # 3. 提示用户输入
        if prompt_text and allow_input:
            print(f"\n⚠️ 需要配置 {key}")
            print(f"💡 提示：可以设置环境变量 {env_var_name} 来避免每次输入")

            if "密码" in prompt_text:
                value = getpass.getpass(f"{prompt_text}: ")
            else:
                value = input(f"{prompt_text}: ").strip()

            if value:
                # 加密并保存到配置文件
                encrypted_value = self.encrypt_value(value)
                self.config.set(section, key, encrypted_value)
                self.save_config()
                print(f"✅ {key} 已加密保存到配置文件")
                return value
        
        return ""
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_payment_password(self, required=True, allow_input=True):
        """获取支付密码"""
        password = self.get_secure_value(
            section='account',
            key='payment_pwd',
            env_var_name='JD_PAYMENT_PWD',
            prompt_text='请输入京东支付密码（6位数字）' if required else None,
            allow_input=allow_input
        )

        if required and not password:
            print("\n" + "="*60)
            print("❌ 错误：支付密码未配置！")
            print("="*60)
            print("支付密码是必须的，用于自动支付订单。")
            print("\n🔧 配置方法：")
            print("方法1 - 环境变量（推荐）：")
            print("  Windows: set JD_PAYMENT_PWD=123456")
            print("  Linux/Mac: export JD_PAYMENT_PWD=123456")
            print("\n方法2 - 配置文件：")
            print("  在config.ini的[account]部分设置：")
            print("  payment_pwd = \"123456\"")
            print("\n方法3 - 运行时输入：")
            print("  重新运行程序，按提示输入密码")
            print("="*60)
            raise ValueError("支付密码未配置，程序无法继续执行")

        return password

    def get_sckey(self, required=True, allow_input=True, interactive=False):
        """获取Server酱密钥"""
        sckey = self.get_secure_value(
            section='messenger',
            key='sckey',
            env_var_name='JD_SCKEY',
            prompt_text=None,  # 不直接提示输入，先询问用户意愿
            allow_input=False  # 先不允许输入
        )

        if required and not sckey and interactive and allow_input:
            # 询问用户是否需要配置SCKEY
            print("\n" + "="*60)
            print("🔔 微信通知配置")
            print("="*60)
            print("微信通知已启用但SCKEY未配置。")
            print("SCKEY用于发送抢购结果和付款提醒到您的微信。")
            print("\n💡 如何获取SCKEY：")
            print("  访问 https://sct.ftqq.com/ 注册并获取SCKEY")
            print("="*60)

            while True:
                choice = input("是否现在配置SCKEY？(yes/no): ").strip().lower()
                if choice in ['yes', 'y', '是', '1']:
                    # 用户选择配置SCKEY
                    print("\n请输入您的Server酱SCKEY：")
                    print("格式示例：SCT123456ABCDEF...")
                    sckey = input("SCKEY: ").strip()

                    if sckey:
                        # 验证SCKEY格式
                        if self._validate_sckey_format(sckey):
                            # 加密并保存到配置文件
                            encrypted_value = self.encrypt_value(sckey)
                            self.config.set('messenger', 'sckey', encrypted_value)
                            self.save_config()
                            print("✅ SCKEY已加密保存到配置文件")
                            return sckey
                        else:
                            print("❌ SCKEY格式不正确，请重新输入")
                            continue
                    else:
                        print("❌ SCKEY不能为空，请重新输入")
                        continue

                elif choice in ['no', 'n', '否', '0']:
                    # 用户选择不配置
                    print("⚠️ 已跳过SCKEY配置，将无法发送微信通知")
                    print("您可以稍后在config.ini中手动配置或设置环境变量JD_SCKEY")
                    return None
                else:
                    print("请输入 yes 或 no")
                    continue

        elif required and not sckey:
            print("\n⚠️ 微信通知已启用但SCKEY未配置，将无法发送通知")
            print("💡 提示：可以设置环境变量 JD_SCKEY 或在config.ini中配置")

        return sckey

    def _validate_sckey_format(self, sckey):
        """验证SCKEY格式"""
        if not sckey:
            return False

        # Server酱新版SCKEY格式：SCT开头，后跟字母数字
        if sckey.startswith('SCT') and len(sckey) > 10:
            return True

        # 旧版格式：纯字母数字组合
        if len(sckey) > 10 and sckey.replace('_', '').replace('-', '').isalnum():
            return True

        return False
    
    def update_device_params(self, eid=None, fp=None):
        """更新设备参数"""
        updated = False
        
        if eid:
            try:
                old_eid = self.config.get('config', 'eid') if self.config.has_option('config', 'eid') else ""
            except:
                old_eid = ""
            if old_eid != eid:
                self.config.set('config', 'eid', eid)
                print(f"✅ 更新设备参数 eid: {eid[:20]}...")
                updated = True

        if fp:
            try:
                old_fp = self.config.get('config', 'fp') if self.config.has_option('config', 'fp') else ""
            except:
                old_fp = ""
            if old_fp != fp:
                self.config.set('config', 'fp', fp)
                print(f"✅ 更新设备参数 fp: {fp[:20]}...")
                updated = True
        
        if updated:
            self.save_config()
            print("✅ 设备参数已自动更新到配置文件")
        
        return updated
