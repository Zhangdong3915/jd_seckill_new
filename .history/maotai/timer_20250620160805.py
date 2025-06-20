# -*- coding:utf-8 -*-
import time
import requests
import json

from datetime import datetime
from maotai.jd_logger import logger
from maotai.config import global_config


class Timer(object):
    def __init__(self, sleep_interval=0.5):
        # '2018-09-28 22:45:50.000'
        # buy_time = 2020-12-22 09:59:59.500
        localtime = time.localtime(time.time())
        buy_time_everyday = global_config.getRaw('config', 'buy_time').__str__()
        last_purchase_time_everyday = global_config.getRaw('config', 'last_purchase_time').__str__()

        # 最后购买时间
        last_purchase_time = datetime.strptime(
            localtime.tm_year.__str__() + '-' + localtime.tm_mon.__str__() + '-' + localtime.tm_mday.__str__() + ' ' + last_purchase_time_everyday,
            "%Y-%m-%d %H:%M:%S.%f")

        buy_time_config = datetime.strptime(
            localtime.tm_year.__str__() + '-' + localtime.tm_mon.__str__() + '-' + localtime.tm_mday.__str__() + ' ' + buy_time_everyday,
            "%Y-%m-%d %H:%M:%S.%f")

        if time.mktime(localtime) < time.mktime(buy_time_config.timetuple()):
            # 取正确的购买时间
            self.buy_time = buy_time_config
        # elif time.mktime(localtime) > time.mktime(last_purchase_time.timetuple()):
        #     # 取明天的时间 购买时间
        #     self.buy_time = datetime.strptime(
        #         localtime.tm_year.__str__() + '-' + localtime.tm_mon.__str__() + '-' + (
        #                 localtime.tm_mday + 1).__str__() + ' ' + buy_time_everyday,
        #         "%Y-%m-%d %H:%M:%S.%f")
        else:
            self.buy_time = datetime.strptime(
                localtime.tm_year.__str__() + '-' + localtime.tm_mon.__str__() + '-' + (
                        localtime.tm_mday + 1).__str__() + ' ' + buy_time_everyday,
                "%Y-%m-%d %H:%M:%S.%f")

        # self.buy_time = buy_time_config
        print("购买时间：{}".format(self.buy_time))

        self.buy_time_ms = int(time.mktime(self.buy_time.timetuple()) * 1000.0 + self.buy_time.microsecond / 1000)
        self.sleep_interval = sleep_interval

        self.diff_time = self.local_jd_time_diff()

    def jd_time(self):
        """
        获取网络时间毫秒（多种备选方案）
        :return:
        """
        # 尝试多个时间源
        time_sources = [
            self._get_jd_time_from_page,
            self._get_time_from_worldclock,
            self._get_time_from_beijing_time,
            self._get_local_time_as_fallback
        ]

        for source in time_sources:
            try:
                result = source()
                if result:
                    return result
            except Exception as e:
                logger.debug(f'时间源 {source.__name__} 失败: {e}')
                continue

        # 所有方案都失败，使用本地时间
        logger.warning('所有网络时间源都失败，使用本地时间')
        return self.local_time()

    def _get_jd_time_from_page(self):
        """从京东页面获取时间"""
        url = 'https://www.jd.com'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=3)
        if resp.status_code == 200:
            # 从响应头获取服务器时间
            server_time = resp.headers.get('Date')
            if server_time:
                from datetime import datetime
                import email.utils
                dt = email.utils.parsedate_to_datetime(server_time)
                return int(dt.timestamp() * 1000)
        return None

    def _get_time_from_worldclock(self):
        """从世界时钟API获取北京时间"""
        url = 'http://worldclockapi.com/api/json/asia/shanghai/now'
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            time_str = data.get('currentDateTime')
            if time_str:
                from datetime import datetime
                # 解析ISO格式时间
                dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                return int(dt.timestamp() * 1000)
        return None

    def _get_time_from_beijing_time(self):
        """从北京时间API获取时间"""
        url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            timestamp = data.get('data', {}).get('t')
            if timestamp:
                return int(timestamp)
        return None

    def _get_local_time_as_fallback(self):
        """本地时间作为最后备选"""
        logger.info('使用本地时间作为时间源')
        return self.local_time()

    def local_time(self):
        """
        获取本地毫秒时间
        :return:
        """
        return int(round(time.time() * 1000))

    def local_jd_time_diff(self):
        """
        计算本地与京东服务器时间差
        :return:
        """
        return self.local_time() - self.jd_time()

    def start(self):
        logger.info('正在等待到达设定时间:{}，检测本地时间与京东服务器时间误差为【{}】毫秒'.format(self.buy_time, self.diff_time))
        while True:
            # 本地时间减去与京东的时间差，能够将时间误差提升到0.1秒附近
            # 具体精度依赖获取京东服务器时间的网络时间损耗
            if self.local_time() - self.diff_time >= self.buy_time_ms:
                logger.info('时间到达，开始执行……')
                break
            else:
                time.sleep(self.sleep_interval)
