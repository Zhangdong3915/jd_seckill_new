import os
import configparser
import threading


class Config(object):
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')
        self._lock = threading.Lock()

    def get(self, section, name):
        with self._lock:
            return self._config.get(section, name)

    def getRaw(self, section, name):
        with self._lock:
            return self._configRaw.get(section, name)

    def reload_config(self):
        """重新加载配置文件"""
        with self._lock:
            try:
                self._config = configparser.ConfigParser()
                self._config.read(self._path, encoding='utf-8-sig')
                self._configRaw = configparser.RawConfigParser()
                self._configRaw.read(self._path, encoding='utf-8-sig')
                print("✅ 配置文件已重新加载")
                return True
            except Exception as e:
                print(f"❌ 配置文件重新加载失败: {e}")
                return False

    def get_config_path(self):
        """获取配置文件路径"""
        return self._path


global_config = Config()
