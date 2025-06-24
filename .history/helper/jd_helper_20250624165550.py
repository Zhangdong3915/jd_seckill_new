import json
import random
import requests
import os
import time

from maotai.config import global_config
from maotai.jd_logger import logger

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
    "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"
]


def parse_json(s):
    """
    解析JSON字符串，支持JSONP格式
    """
    try:
        # 首先尝试直接解析JSON
        return json.loads(s)
    except json.JSONDecodeError:
        # 如果失败，尝试提取JSONP中的JSON部分
        if '(' in s and ')' in s:
            # JSONP格式: callback({"key": "value"})
            start = s.find('(') + 1
            end = s.rfind(')')
            if start > 0 and end > start:
                json_str = s[start:end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass

        # 尝试原始方法：查找第一个{到最后一个}
        begin = s.find('{')
        end = s.rfind('}') + 1
        if begin >= 0 and end > begin:
            try:
                return json.loads(s[begin:end])
            except json.JSONDecodeError:
                pass

        # 如果都失败了，抛出异常并包含更多信息
        raise json.JSONDecodeError(
            f"无法解析JSON，内容类型可能不正确。内容前100字符: {s[:100]}",
            s, 0
        )


def get_random_useragent():
    """生成随机的UserAgent
    :return: UserAgent字符串
    """
    return random.choice(USER_AGENTS)


def wait_some_time():
    """安全智能等待时间 - 防风控优化"""
    from datetime import datetime

    now = datetime.now()

    # 秒杀时间段使用适中间隔（防风控）
    if 11 <= now.hour <= 12 and 55 <= now.minute <= 35:
        # 秒杀时间：100-500ms随机间隔（安全范围）
        base_interval = random.randint(100, 500) / 1000
        # 添加随机波动，模拟人类行为
        random_factor = random.uniform(0.8, 1.5)
        time.sleep(base_interval * random_factor)
    else:
        # 平时：200-800ms随机间隔
        base_interval = random.randint(200, 800) / 1000
        random_factor = random.uniform(0.9, 1.2)
        time.sleep(base_interval * random_factor)


def send_wechat(message):
    """推送信息到微信"""
    # 使用安全配置管理器获取解密后的SCKEY
    try:
        from helper.secure_config import SecureConfigManager
        secure_config = SecureConfigManager()
        sckey = secure_config.get_secure_value(
            section='messenger',
            key='sckey',
            env_var_name='JD_SCKEY',
            prompt_text=None,
            allow_input=False
        )
    except:
        # 备用方案：直接从配置文件读取（可能是加密的）
        sckey = global_config.getRaw('messenger', 'sckey')

    if not sckey:
        logger.warning('SCKEY未配置，无法发送微信通知')
        return

    # 判断是新版还是旧版Server酱
    if sckey.startswith('SCT'):
        # 新版Server酱Turbo API
        url = 'https://sctapi.ftqq.com/{}.send'.format(sckey)
    else:
        # 旧版Server酱API
        url = 'http://sc.ftqq.com/{}.send'.format(sckey)

    payload = {
        "text": '京东秒杀通知',
        "desp": message
    }
    headers = {
        'User-Agent': global_config.getRaw('config', 'DEFAULT_USER_AGENT')
    }

    try:
        resp = requests.get(url, params=payload, headers=headers, timeout=10)
        logger.info(f'微信推送发送完成，状态码: {resp.status_code}')
        if resp.status_code == 200:
            try:
                result = resp.json()
                if result.get('code') == 0:
                    logger.info('微信推送发送成功')
                else:
                    logger.warning(f'微信推送发送失败: {result.get("message", "未知错误")}')
            except:
                logger.info('微信推送已发送，但响应格式异常')
        else:
            logger.warning(f'微信推送发送失败，HTTP状态码: {resp.status_code}')
    except Exception as e:
        logger.error(f'微信推送发送异常: {e}')


def response_status(resp):
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


def open_image(image_file):
    if os.name == "nt":
        os.system('start ' + image_file)  # for Windows
    else:
        if os.uname()[0] == "Linux":
            if "deepin" in os.uname()[2]:
                os.system("deepin-image-viewer " + image_file)  # for deepin
            else:
                os.system("eog " + image_file)  # for Linux
        else:
            os.system("open " + image_file)  # for Mac


def save_image(resp, image_file):
    with open(image_file, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            f.write(chunk)


def close_image_windows():
    """
    关闭二维码图片窗口
    专门针对qr_code.png文件的窗口进行关闭
    """
    import subprocess
    import time
    import psutil

    try:
        if os.name == "nt":  # Windows
            print("正在关闭二维码窗口...")

            # 方法1: 使用PowerShell查找并关闭包含qr_code.png的窗口
            try:
                # 查找包含qr_code.png的窗口并关闭
                powershell_cmd = '''
                Get-Process | Where-Object {$_.MainWindowTitle -like "*qr_code*"} | Stop-Process -Force
                '''
                subprocess.run([
                    'powershell', '-Command', powershell_cmd
                ], capture_output=True, check=False, timeout=5)
                print("已尝试通过窗口标题关闭二维码窗口")
            except Exception as e:
                print(f"PowerShell方法失败: {e}")

            # 方法2: 关闭常见的图片查看器进程
            image_viewers = [
                'Microsoft.Photos.exe',  # Windows 10/11 照片应用
                'PhotosApp.exe',         # 照片应用的另一个名称
                'Photos.exe',            # 简化名称
                'mspaint.exe',           # 画图
                'WindowsPhotoViewer.exe', # Windows照片查看器
                'dllhost.exe',           # 有时照片查看器使用这个进程
                'IrfanView.exe',         # IrfanView
                'HoneyView.exe',         # HoneyView
                'nomacs.exe',            # nomacs
                'XnView.exe'             # XnView
            ]

            closed_any = False
            for viewer in image_viewers:
                try:
                    result = subprocess.run([
                        'taskkill', '/F', '/IM', viewer
                    ], capture_output=True, check=False, timeout=3)

                    if result.returncode == 0:
                        print(f"已关闭进程: {viewer}")
                        closed_any = True
                except Exception as e:
                    continue

            # 方法3: 使用psutil查找并关闭相关进程
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        # 检查进程命令行是否包含qr_code.png
                        if proc.info['cmdline']:
                            cmdline = ' '.join(proc.info['cmdline']).lower()
                            if 'qr_code.png' in cmdline or 'qr_code' in cmdline:
                                proc.terminate()
                                print(f"已终止包含qr_code的进程: {proc.info['name']} (PID: {proc.info['pid']})")
                                closed_any = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
            except Exception as e:
                print(f"psutil方法失败: {e}")

            # 方法4: 删除并重新创建qr_code.png文件来强制关闭
            try:
                qr_file = "qr_code.png"
                if os.path.exists(qr_file):
                    # 先尝试重命名文件，这会强制关闭打开它的程序
                    temp_file = "qr_code_temp.png"
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    os.rename(qr_file, temp_file)
                    time.sleep(0.5)
                    # 删除临时文件
                    os.remove(temp_file)
                    print("已通过文件操作强制关闭二维码窗口")
                    closed_any = True
            except Exception as e:
                print(f"文件操作方法失败: {e}")

            if closed_any:
                print("二维码窗口已自动关闭")
            else:
                print("未找到需要关闭的二维码窗口，可能已经关闭")

        else:  # Linux/Mac
            if os.uname()[0] == "Linux":
                if "deepin" in os.uname()[2]:
                    subprocess.run(['pkill', 'deepin-image-viewer'], capture_output=True, check=False)
                else:
                    subprocess.run(['pkill', 'eog'], capture_output=True, check=False)
            else:  # Mac
                subprocess.run(['pkill', 'Preview'], capture_output=True, check=False)
            print("二维码窗口已自动关闭")

    except Exception as e:
        print(f"关闭二维码窗口时发生异常: {e}")
        print("请手动关闭二维码窗口")