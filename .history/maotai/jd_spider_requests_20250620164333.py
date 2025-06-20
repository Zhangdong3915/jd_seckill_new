import random
import time
import requests
import functools
import json
import os
import pickle

from lxml import etree

from error.exception import SKException
from maotai.jd_logger import logger
from maotai.timer import Timer
from maotai.config import global_config
from concurrent.futures import ProcessPoolExecutor
from helper.jd_helper import (
    parse_json,
    send_wechat,
    wait_some_time,
    response_status,
    save_image,
    open_image
)


class SpiderSession:
    """
    Session相关操作
    """

    def __init__(self):
        self.cookies_dir_path = "./cookies/"
        self.user_agent = global_config.getRaw('config', 'DEFAULT_USER_AGENT')

        self.session = self._init_session()

    def _init_session(self):
        session = requests.session()
        session.headers = self.get_headers()
        return session

    def get_headers(self):
        return {"User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;"
                          "q=0.9,image/webp,image/apng,*/*;"
                          "q=0.8,application/signed-exchange;"
                          "v=b3",
                "Connection": "keep-alive"}

    def get_user_agent(self):
        return self.user_agent

    def get_session(self):
        """
        获取当前Session
        :return:
        """
        return self.session

    def get_cookies(self):
        """
        获取当前Cookies
        :return:
        """
        return self.get_session().cookies

    def set_cookies(self, cookies):
        self.session.cookies.update(cookies)

    def load_cookies_from_local(self):
        """
        从本地加载Cookie
        :return:
        """
        cookies_file = ''
        if not os.path.exists(self.cookies_dir_path):
            return False
        for name in os.listdir(self.cookies_dir_path):
            if name.endswith(".cookies"):
                cookies_file = '{}{}'.format(self.cookies_dir_path, name)
                break
        if cookies_file == '':
            return False
        with open(cookies_file, 'rb') as f:
            local_cookies = pickle.load(f)
        self.set_cookies(local_cookies)

    def save_cookies_to_local(self, cookie_file_name):
        """
        保存Cookie到本地
        :param cookie_file_name: 存放Cookie的文件名称
        :return:
        """
        cookies_file = '{}{}.cookies'.format(self.cookies_dir_path, cookie_file_name)
        directory = os.path.dirname(cookies_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(cookies_file, 'wb') as f:
            pickle.dump(self.get_cookies(), f)


class QrLogin:
    """
    扫码登录
    """

    def __init__(self, spider_session: SpiderSession):
        """
        初始化扫码登录
        大致流程：
            1、访问登录二维码页面，获取Token
            2、使用Token获取票据
            3、校验票据
        :param spider_session:
        """
        self.qrcode_img_file = '../qr_code.png'

        self.spider_session = spider_session
        self.session = self.spider_session.get_session()

        self.is_login = False
        self.refresh_login_status()

    def refresh_login_status(self):
        """
        刷新是否登录状态
        :return:
        """
        self.is_login = self._validate_cookies()

    def _validate_cookies(self):
        """
        验证cookies是否有效（是否登陆）
        通过访问用户订单列表页进行判断：若未登录，将会重定向到登陆页面。
        :return: cookies是否有效 True/False
        """
        url = 'https://order.jd.com/center/list.action'
        payload = {
            'rid': str(int(time.time() * 1000)),
        }
        try:
            resp = self.session.get(url=url, params=payload, allow_redirects=False)
            logger.debug(f'登录验证响应状态: {resp.status_code}')
            logger.debug(f'登录验证响应头: {resp.headers.get("Location", "无重定向")}')

            # 检查是否被重定向到登录页面
            if resp.status_code == 302:
                location = resp.headers.get('Location', '')
                if 'passport.jd.com' in location or 'login' in location.lower():
                    logger.info('检测到重定向到登录页面，用户未登录')
                    return False
            elif resp.status_code == requests.codes.OK:
                # 检查页面内容是否包含登录相关信息
                if '登录' in resp.text or 'login' in resp.text.lower():
                    logger.info('页面包含登录信息，用户可能未登录')
                    return False
                return True
        except Exception as e:
            logger.error(f"验证cookies是否有效发生异常: {e}")
        return False

    def _get_login_page(self):
        """
        获取PC端登录页面
        :return:
        """
        url = "https://passport.jd.com/new/login.aspx"
        page = self.session.get(url, headers=self.spider_session.get_headers())
        return page

    def _get_qrcode(self):
        """
        缓存并展示登录二维码
        :return:
        """
        url = 'https://qr.m.jd.com/show'
        payload = {
            'appid': 133,
            'size': 147,
            't': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.spider_session.get_user_agent(),
            'Referer': 'https://passport.jd.com/new/login.aspx',
        }
        resp = self.session.get(url=url, headers=headers, params=payload)

        if not response_status(resp):
            logger.info('获取二维码失败')
            return False

        save_image(resp, self.qrcode_img_file)
        print("\n📱 二维码已生成")
        print("请使用京东APP扫描二维码完成登录")
        print("二维码图片已自动打开，如未显示请手动打开：qr_code.png")
        logger.info('二维码获取成功，请打开京东APP扫描')
        open_image(self.qrcode_img_file)
        return True

    def _get_qrcode_ticket(self):
        """
        通过 token 获取票据
        :return:
        """
        url = 'https://qr.m.jd.com/check'
        payload = {
            'appid': '133',
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            'token': self.session.cookies.get('wlfstk_smdl'),
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.spider_session.get_user_agent(),
            'Referer': 'https://passport.jd.com/new/login.aspx',
        }
        resp = self.session.get(url=url, headers=headers, params=payload)

        if not response_status(resp):
            logger.error('获取二维码扫描结果异常')
            return False

        resp_json = parse_json(resp.text)
        if resp_json['code'] != 200:
            logger.info('Code: %s, Message: %s', resp_json['code'], resp_json['msg'])
            return None
        else:
            logger.info('已完成手机客户端确认')
            return resp_json['ticket']

    def _validate_qrcode_ticket(self, ticket):
        """
        通过已获取的票据进行校验
        :param ticket: 已获取的票据
        :return:
        """
        url = 'https://passport.jd.com/uc/qrCodeTicketValidation'
        headers = {
            'User-Agent': self.spider_session.get_user_agent(),
            'Referer': 'https://passport.jd.com/uc/login?ltype=logout',
        }

        resp = self.session.get(url=url, headers=headers, params={'t': ticket})
        if not response_status(resp):
            return False

        resp_json = json.loads(resp.text)
        if resp_json['returnCode'] == 0:
            return True
        else:
            logger.info(resp_json)
            return False

    def login_by_qrcode(self):
        """
        二维码登陆
        :return:
        """
        self._get_login_page()

        # download QR code
        if not self._get_qrcode():
            raise SKException('二维码下载失败')

        # get QR code ticket
        ticket = None
        retry_times = 85
        for _ in range(retry_times):
            ticket = self._get_qrcode_ticket()
            if ticket:
                break
            time.sleep(2)
        else:
            raise SKException('二维码过期，请重新获取扫描')

        # validate QR code ticket
        if not self._validate_qrcode_ticket(ticket):
            raise SKException('二维码信息校验失败')

        self.refresh_login_status()

        logger.info('二维码登录成功')


class JdSeckill(object):
    def __init__(self):
        self.spider_session = SpiderSession()
        self.spider_session.load_cookies_from_local()

        self.qrlogin = QrLogin(self.spider_session)

        # 初始化信息
        self.sku_id = global_config.getRaw('config', 'sku_id')
        self.seckill_num = global_config.getRaw('config', 'seckill_num')
        self.seckill_init_info = dict()
        self.seckill_url = dict()
        self.seckill_order_data = dict()
        self.timers = Timer()

        self.session = self.spider_session.get_session()
        self.user_agent = self.spider_session.user_agent
        self.nick_name = None

        # 自动化模式相关属性
        self.auto_mode_running = False
        self.login_check_interval = 300  # 5分钟检查一次登录状态
        self.last_login_check = 0

    def login_by_qrcode(self):
        """
        二维码登陆
        :return:
        """
        if self.qrlogin.is_login:
            print("✅ 用户已登录")
            logger.info('登录成功')
            return

        self.qrlogin.login_by_qrcode()

        if self.qrlogin.is_login:
            self.nick_name = self.get_username()
            self.spider_session.save_cookies_to_local(self.nick_name)
            print("\n" + "="*60)
            print("✅ 登录成功")
            print("="*60)
            print(f"欢迎，{self.nick_name}！")
            print("程序将继续执行...")
            print("="*60)
        else:
            print("\n❌ 登录失败，请重试")
            raise SKException("二维码登录失败！")

    def check_login(func):
        """
        用户登陆态校验装饰器。若用户未登陆，则调用扫码登陆
        """

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            if not self.qrlogin.is_login:
                print("\n" + "="*60)
                print("🔐 账号未登录")
                print("="*60)
                print("请使用京东APP扫描二维码完成登录")
                print("登录成功后程序将自动继续执行")
                print("="*60)
                logger.info("{0} 需登陆后调用，开始扫码登陆".format(func.__name__))
                self.login_by_qrcode()
            return func(self, *args, **kwargs)

        return new_func

    @check_login
    def reserve(self):
        """
        预约
        """
        self._reserve()

    @check_login
    def seckill(self):
        """
        抢购
        """
        self._seckill()

    @check_login
    def seckill_by_proc_pool(self, work_count=5):
        """
        多进程进行抢购
        work_count：进程数量
        """
        with ProcessPoolExecutor(work_count) as pool:
            for i in range(work_count):
                pool.submit(self.seckill)

    def _reserve(self):
        """
        预约
        """
        while True:
            try:
                self.make_reserve()
                break
            except Exception as e:
                logger.info(f'预约发生异常: {str(e)}')
            wait_some_time()

    def _seckill(self):
        """
        抢购
        """
        while True:
            try:
                self.request_seckill_url()
                while True:
                    self.request_seckill_checkout_page()
                    self.submit_seckill_order()
            except Exception as e:
                logger.info(f'抢购发生异常，稍后继续执行: {str(e)}')
            wait_some_time()

    def make_reserve(self):
        """商品预约"""
        logger.info('商品名称:{}'.format(self.get_sku_title()))
        url = 'https://yushou.jd.com/youshouinfo.action'
        payload = {
            'callback': 'fetchJSON',
            'sku': self.sku_id,
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
        }
        resp = self.session.get(url=url, params=payload, headers=headers)

        # 检查响应内容类型
        content_type = resp.headers.get('Content-Type', '')
        logger.info(f'预约接口响应类型: {content_type}')
        logger.info(f'预约接口响应状态: {resp.status_code}')

        # 如果返回的是HTML页面，说明接口可能失效或需要登录
        if 'text/html' in content_type:
            logger.warning('预约接口返回HTML页面，可能需要登录或接口已失效')
            if '登录' in resp.text or 'login' in resp.text.lower():
                print("\n" + "="*60)
                print("🔐 登录已过期")
                print("="*60)
                print("检测到登录状态已过期，需要重新登录")
                print("请使用京东APP扫描二维码重新登录")
                print("="*60)
                logger.info('检测到需要重新登录，开始二维码登录流程')
                # 重新登录
                self.qrlogin.is_login = False  # 强制重新登录
                self.login_by_qrcode()
                # 重新尝试预约
                resp = self.session.get(url=url, params=payload, headers=headers)
                content_type = resp.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    raise Exception('重新登录后预约接口仍然失效')
            else:
                raise Exception('预约接口可能已失效，返回了HTML页面而非JSON数据')

        try:
            resp_json = parse_json(resp.text)
            logger.info(f'预约接口返回数据: {resp_json}')
        except Exception as e:
            logger.error(f'解析预约接口响应失败: {e}')
            logger.error(f'响应内容前200字符: {resp.text[:200]}')
            raise Exception(f'预约接口响应格式错误: {e}')

        reserve_url = resp_json.get('url')
        if not reserve_url:
            logger.error('预约接口未返回预约URL')
            raise Exception('预约接口未返回有效的预约URL')
        self.timers.start()
        while True:
            try:
                self.session.get(url='https:' + reserve_url)
                logger.info('预约成功，已获得抢购资格 / 您已成功预约过了，无需重复预约')
                if global_config.getRaw('messenger', 'enable') == 'true':
                    success_message = "预约成功，已获得抢购资格 / 您已成功预约过了，无需重复预约"
                    send_wechat(success_message)
                break
            except Exception as e:
                logger.error('预约失败正在重试...')

    def get_username(self):
        """获取用户信息"""
        url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action'
        payload = {
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://order.jd.com/center/list.action',
        }

        resp = self.session.get(url=url, params=payload, headers=headers)

        try_count = 5
        while not resp.text.startswith("jQuery"):
            try_count = try_count - 1
            if try_count > 0:
                resp = self.session.get(url=url, params=payload, headers=headers)
            else:
                break
            wait_some_time()
        # 响应中包含了许多用户信息，现在在其中返回昵称
        # jQuery2381773({"imgUrl":"//storage.360buyimg.com/i.imageUpload/xxx.jpg","lastLoginTime":"","nickName":"xxx","plusStatus":"0","realName":"xxx","userLevel":x,"userScoreVO":{"accountScore":xx,"activityScore":xx,"consumptionScore":xxxxx,"default":false,"financeScore":xxx,"pin":"xxx","riskScore":x,"totalScore":xxxxx}})
        return parse_json(resp.text).get('nickName')

    def get_sku_title(self):
        """获取商品名称"""
        url = 'https://item.jd.com/{}.html'.format(global_config.getRaw('config', 'sku_id'))
        resp = self.session.get(url).content
        x_data = etree.HTML(resp)
        sku_title = x_data.xpath('/html/head/title/text()')
        return sku_title[0]

    def get_seckill_url(self):
        """获取商品的抢购链接
        点击"抢购"按钮后，会有两次302跳转，最后到达订单结算页面
        这里返回第一次跳转后的页面url，作为商品的抢购链接
        :return: 商品的抢购链接
        """
        url = 'https://itemko.jd.com/itemShowBtn'
        payload = {
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            'skuId': self.sku_id,
            'from': 'pc',
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'itemko.jd.com',
            'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
        }
        while True:
            resp = self.session.get(url=url, headers=headers, params=payload)
            resp_json = parse_json(resp.text)
            if resp_json.get('url'):
                # https://divide.jd.com/user_routing?skuId=8654289&sn=c3f4ececd8461f0e4d7267e96a91e0e0&from=pc
                router_url = 'https:' + resp_json.get('url')
                # https://marathon.jd.com/captcha.html?skuId=8654289&sn=c3f4ececd8461f0e4d7267e96a91e0e0&from=pc
                seckill_url = router_url.replace(
                    'divide', 'marathon').replace(
                    'user_routing', 'captcha.html')
                logger.info("抢购链接获取成功: %s", seckill_url)
                return seckill_url
            else:
                logger.info("抢购链接获取失败，稍后自动重试")
                wait_some_time()

    def request_seckill_url(self):
        """访问商品的抢购链接（用于设置cookie等"""
        logger.info('用户:{}'.format(self.get_username()))
        logger.info('商品名称:{}'.format(self.get_sku_title()))
        self.timers.start()
        self.seckill_url[self.sku_id] = self.get_seckill_url()
        logger.info('访问商品的抢购连接...')
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'marathon.jd.com',
            'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
        }
        self.session.get(
            url=self.seckill_url.get(
                self.sku_id),
            headers=headers,
            allow_redirects=False)

    def request_seckill_checkout_page(self):
        """访问抢购订单结算页面"""
        logger.info('访问抢购订单结算页面...')
        url = 'https://marathon.jd.com/seckill/seckill.action'
        payload = {
            'skuId': self.sku_id,
            'num': self.seckill_num,
            'rid': int(time.time())
        }
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'marathon.jd.com',
            'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
        }
        self.session.get(url=url, params=payload, headers=headers, allow_redirects=False)

    def _get_seckill_init_info(self):
        """获取秒杀初始化信息（包括：地址，发票，token）
        :return: 初始化信息组成的dict
        """
        logger.info('获取秒杀初始化信息...')
        url = 'https://marathon.jd.com/seckillnew/orderService/pc/init.action'
        data = {
            'sku': self.sku_id,
            'num': self.seckill_num,
            'isModifyAddress': 'false',
        }
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'marathon.jd.com',
        }
        resp = self.session.post(url=url, data=data, headers=headers)

        resp_json = None
        try:
            resp_json = parse_json(resp.text)
        except Exception:
            raise SKException('抢购失败，返回信息:{}'.format(resp.text[0: 128]))

        return resp_json

    def _get_seckill_order_data(self):
        """生成提交抢购订单所需的请求体参数
        :return: 请求体参数组成的dict
        """
        logger.info('生成提交抢购订单所需参数...')
        # 获取用户秒杀初始化信息
        self.seckill_init_info[self.sku_id] = self._get_seckill_init_info()
        init_info = self.seckill_init_info.get(self.sku_id)
        default_address = init_info['addressList'][0]  # 默认地址dict
        invoice_info = init_info.get('invoiceInfo', {})  # 默认发票信息dict, 有可能不返回
        token = init_info['token']
        data = {
            'skuId': self.sku_id,
            'num': self.seckill_num,
            'addressId': default_address['id'],
            'yuShou': 'true',
            'isModifyAddress': 'false',
            'name': default_address['name'],
            'provinceId': default_address['provinceId'],
            'cityId': default_address['cityId'],
            'countyId': default_address['countyId'],
            'townId': default_address['townId'],
            'addressDetail': default_address['addressDetail'],
            'mobile': default_address['mobile'],
            'mobileKey': default_address['mobileKey'],
            'email': default_address.get('email', ''),
            'postCode': '',
            'invoiceTitle': invoice_info.get('invoiceTitle', -1),
            'invoiceCompanyName': '',
            'invoiceContent': invoice_info.get('invoiceContentType', 1),
            'invoiceTaxpayerNO': '',
            'invoiceEmail': '',
            'invoicePhone': invoice_info.get('invoicePhone', ''),
            'invoicePhoneKey': invoice_info.get('invoicePhoneKey', ''),
            'invoice': 'true' if invoice_info else 'false',
            'password': global_config.get('account', 'payment_pwd'),
            'codTimeType': 3,
            'paymentType': 4,
            'areaCode': '',
            'overseas': 0,
            'phone': '',
            'eid': global_config.getRaw('config', 'eid'),
            'fp': global_config.getRaw('config', 'fp'),
            'token': token,
            'pru': ''
        }

        return data

    def submit_seckill_order(self):
        """提交抢购（秒杀）订单
        :return: 抢购结果 True/False
        """
        url = 'https://marathon.jd.com/seckillnew/orderService/pc/submitOrder.action'
        payload = {
            'skuId': self.sku_id,
        }
        try:
            self.seckill_order_data[self.sku_id] = self._get_seckill_order_data()
        except Exception as e:
            logger.info('抢购失败，无法获取生成订单的基本信息，接口返回:【{}】'.format(str(e)))
            return False

        logger.info('提交抢购订单...')
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'marathon.jd.com',
            'Referer': 'https://marathon.jd.com/seckill/seckill.action?skuId={0}&num={1}&rid={2}'.format(
                self.sku_id, self.seckill_num, int(time.time())),
        }
        resp = self.session.post(
            url=url,
            params=payload,
            data=self.seckill_order_data.get(
                self.sku_id),
            headers=headers)
        resp_json = None
        try:
            resp_json = parse_json(resp.text)
        except Exception as e:
            logger.info('抢购失败，返回信息:{}'.format(resp.text[0: 128]))
            return False
        # 返回信息
        # 抢购失败：
        # {'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 60074, 'skuId': 0, 'success': False}
        # {'errorMessage': '抱歉，您提交过快，请稍后再提交订单！', 'orderId': 0, 'resultCode': 60017, 'skuId': 0, 'success': False}
        # {'errorMessage': '系统正在开小差，请重试~~', 'orderId': 0, 'resultCode': 90013, 'skuId': 0, 'success': False}
        # 抢购成功：
        # {"appUrl":"xxxxx","orderId":820227xxxxx,"pcUrl":"xxxxx","resultCode":0,"skuId":0,"success":true,"totalMoney":"xxxxx"}
        if resp_json.get('success'):
            order_id = resp_json.get('orderId')
            total_money = resp_json.get('totalMoney')
            pay_url = 'https:' + resp_json.get('pcUrl')
            logger.info('抢购成功，订单号:{}, 总价:{}, 电脑端付款链接:{}'.format(order_id, total_money, pay_url))
            if global_config.getRaw('messenger', 'enable') == 'true':
                success_message = "抢购成功，订单号:{}, 总价:{}, 电脑端付款链接:{}".format(order_id, total_money, pay_url)
                send_wechat(success_message)
            return True
        else:
            logger.info('抢购失败，返回信息:{}'.format(resp_json))
            if global_config.getRaw('messenger', 'enable') == 'true':
                error_message = '抢购失败，返回信息:{}'.format(resp_json)
                send_wechat(error_message)
            return False

    def auto_login_maintenance(self):
        """自动登录维护"""
        import time
        current_time = time.time()

        # 检查是否需要验证登录状态
        if current_time - self.last_login_check > self.login_check_interval:
            logger.info('定期检查登录状态...')
            old_status = self.qrlogin.is_login
            self.qrlogin.refresh_login_status()

            if old_status and not self.qrlogin.is_login:
                logger.warning('检测到登录状态失效，开始自动重新登录')
                print("\n" + "="*60)
                print("🔄 登录状态失效，自动重新登录")
                print("="*60)
                print("请使用京东APP扫描二维码重新登录")
                print("登录成功后程序将自动继续")
                print("="*60)

                try:
                    self.login_by_qrcode()
                    if self.qrlogin.is_login:
                        logger.info('自动重新登录成功')
                        print("✅ 自动重新登录成功，程序继续运行")
                    else:
                        logger.error('自动重新登录失败')
                        return False
                except Exception as e:
                    logger.error(f'自动重新登录过程中出现异常: {e}')
                    return False

            self.last_login_check = current_time

        return self.qrlogin.is_login

    def get_time_status(self):
        """获取当前时间状态，判断应该执行什么操作"""
        from datetime import datetime, timedelta
        import time

        now = datetime.now()
        current_time_str = now.strftime('%H:%M:%S.%f')[:-3]  # 精确到毫秒

        # 获取配置的时间
        buy_time_str = global_config.getRaw('config', 'buy_time')
        last_purchase_time_str = global_config.getRaw('config', 'last_purchase_time')

        # 解析时间
        buy_time = datetime.strptime(f"{now.date()} {buy_time_str}", "%Y-%m-%d %H:%M:%S.%f")
        last_purchase_time = datetime.strptime(f"{now.date()} {last_purchase_time_str}", "%Y-%m-%d %H:%M:%S.%f")

        # 如果当前时间已经过了最后购买时间，则考虑明天的时间
        if now > last_purchase_time:
            tomorrow = now.date() + timedelta(days=1)
            buy_time = datetime.strptime(f"{tomorrow} {buy_time_str}", "%Y-%m-%d %H:%M:%S.%f")
            last_purchase_time = datetime.strptime(f"{tomorrow} {last_purchase_time_str}", "%Y-%m-%d %H:%M:%S.%f")

        # 计算时间差
        time_to_buy = (buy_time - now).total_seconds()
        time_to_end = (last_purchase_time - now).total_seconds()

        if time_to_buy > 3600:  # 距离购买时间超过1小时
            return {
                'status': 'waiting_reserve',
                'action': '等待预约时间',
                'time_to_action': time_to_buy,
                'next_action_time': buy_time,
                'description': f'距离预约时间还有 {int(time_to_buy//3600)}小时{int((time_to_buy%3600)//60)}分钟'
            }
        elif time_to_buy > 0:  # 距离购买时间不到1小时，可以开始预约
            return {
                'status': 'reserve_time',
                'action': '执行预约',
                'time_to_action': time_to_buy,
                'next_action_time': buy_time,
                'description': f'预约时间段，距离秒杀还有 {int(time_to_buy//60)}分钟{int(time_to_buy%60)}秒'
            }
        elif time_to_end > 0:  # 在秒杀时间段内
            return {
                'status': 'seckill_time',
                'action': '执行秒杀',
                'time_to_action': 0,
                'next_action_time': buy_time,
                'description': f'秒杀时间段，距离结束还有 {int(time_to_end//60)}分钟{int(time_to_end%60)}秒'
            }
        else:  # 已经过了秒杀时间
            return {
                'status': 'finished',
                'action': '等待明天',
                'time_to_action': 86400 + time_to_buy,  # 明天的时间
                'next_action_time': buy_time,
                'description': '今日秒杀已结束，等待明天'
            }

    def auto_mode(self):
        """全自动化模式 - 预约+秒杀一体化"""
        self.auto_mode_running = True

        print("🚀 全自动化模式已启动")
        print("系统将智能判断当前时间并自动执行相应操作")
        print("支持自动登录维护、错误恢复、跨天执行")
        print("-" * 60)

        # 确保用户已登录
        if not self.qrlogin.is_login:
            print("\n🔐 检测到未登录，开始登录流程")
            self.login_by_qrcode()

        reserve_completed = False
        seckill_completed = False

        while self.auto_mode_running:
            try:
                # 自动登录维护
                if not self.auto_login_maintenance():
                    logger.error('登录维护失败，程序暂停')
                    time.sleep(60)
                    continue

                # 获取当前时间状态
                time_status = self.get_time_status()

                # 显示状态面板
                self.display_status_panel(time_status, reserve_completed, seckill_completed)

                if time_status['status'] == 'waiting_reserve':
                    if not reserve_completed:
                        print("⏳ 等待预约时间...")
                        sleep_time = min(300, time_status['time_to_action'] - 300)  # 提前5分钟准备
                        if sleep_time > 0:
                            print(f"将在 {int(sleep_time)} 秒后重新检查")
                            time.sleep(sleep_time)
                        else:
                            print("即将进入预约时间段")
                            time.sleep(30)
                    else:
                        print("✅ 预约已完成，等待秒杀时间")
                        time.sleep(60)

                elif time_status['status'] == 'reserve_time':
                    if not reserve_completed:
                        print("🎯 开始执行预约...")
                        try:
                            self.safe_reserve()
                            reserve_completed = True
                            self.send_notification("预约成功", "商品预约已完成，等待秒杀时间", "success")
                        except Exception as e:
                            self.send_notification("预约失败", f"预约执行失败: {e}", "error")
                            time.sleep(30)
                    else:
                        print("✅ 预约已完成，等待秒杀时间")
                        time.sleep(30)

                elif time_status['status'] == 'seckill_time':
                    if not seckill_completed:
                        print("🔥 开始执行秒杀...")
                        try:
                            self.safe_seckill()
                            seckill_completed = True
                            self.send_notification("秒杀完成", "秒杀程序已执行完成", "success")
                        except Exception as e:
                            self.send_notification("秒杀异常", f"秒杀执行失败: {e}", "error")
                            time.sleep(10)
                    else:
                        print("✅ 秒杀已完成")
                        time.sleep(60)

                elif time_status['status'] == 'finished':
                    print("🌙 今日任务完成，重置状态等待明天")
                    reserve_completed = False
                    seckill_completed = False
                    # 等待到明天
                    sleep_time = min(3600, time_status['time_to_action'])  # 最多等待1小时
                    print(f"将在 {int(sleep_time)} 秒后重新检查")
                    time.sleep(sleep_time)

            except KeyboardInterrupt:
                print("\n\n🛑 用户中断程序")
                self.auto_mode_running = False
                break
            except Exception as e:
                logger.error(f'全自动化模式发生异常: {e}')
                print(f"⚠️ 发生异常: {e}")
                print("程序将在30秒后重试...")
                time.sleep(30)

        print("🏁 全自动化模式已停止")

    def enhanced_error_handler(self, func, *args, **kwargs):
        """增强的错误处理器"""
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError as e:
                retry_count += 1
                logger.warning(f'网络连接错误 (重试 {retry_count}/{max_retries}): {e}')
                print(f"🌐 网络连接异常，{5 * retry_count}秒后重试...")
                time.sleep(5 * retry_count)
            except requests.exceptions.Timeout as e:
                retry_count += 1
                logger.warning(f'请求超时 (重试 {retry_count}/{max_retries}): {e}')
                print(f"⏱️ 请求超时，{3 * retry_count}秒后重试...")
                time.sleep(3 * retry_count)
            except json.JSONDecodeError as e:
                retry_count += 1
                logger.warning(f'JSON解析错误 (重试 {retry_count}/{max_retries}): {e}')
                print(f"📄 数据格式异常，{2 * retry_count}秒后重试...")
                time.sleep(2 * retry_count)
            except SKException as e:
                logger.error(f'业务逻辑异常: {e}')
                print(f"⚠️ 业务异常: {e}")
                if '登录' in str(e) or 'login' in str(e).lower():
                    print("🔐 检测到登录相关异常，尝试重新登录...")
                    self.qrlogin.is_login = False
                    return None
                raise e
            except Exception as e:
                retry_count += 1
                logger.error(f'未知异常 (重试 {retry_count}/{max_retries}): {e}')
                print(f"❌ 未知异常: {e}")
                if retry_count < max_retries:
                    print(f"将在 {10 * retry_count} 秒后重试...")
                    time.sleep(10 * retry_count)
                else:
                    raise e

        raise Exception(f'操作失败，已重试 {max_retries} 次')

    def safe_reserve(self):
        """安全的预约执行"""
        return self.enhanced_error_handler(self._reserve)

    def safe_seckill(self):
        """安全的秒杀执行"""
        return self.enhanced_error_handler(self._seckill)

    def send_notification(self, title, message, notification_type="info"):
        """发送通知"""
        try:
            # 控制台通知
            icons = {
                "info": "ℹ️",
                "success": "✅",
                "warning": "⚠️",
                "error": "❌"
            }
            icon = icons.get(notification_type, "ℹ️")

            print(f"\n{icon} {title}")
            print(f"   {message}")

            # 微信通知（如果启用）
            if global_config.getRaw('messenger', 'enable') == 'true':
                full_message = f"{title}\n{message}"
                send_wechat(full_message)

            # 日志记录
            if notification_type == "error":
                logger.error(f"{title}: {message}")
            elif notification_type == "warning":
                logger.warning(f"{title}: {message}")
            else:
                logger.info(f"{title}: {message}")

        except Exception as e:
            logger.error(f'发送通知失败: {e}')

    def display_status_panel(self, time_status, reserve_completed, seckill_completed):
        """显示状态面板"""
        from datetime import datetime

        print("\n" + "="*60)
        print("🤖 全自动化模式 - 状态面板")
        print("="*60)
        print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 当前状态: {time_status['description']}")
        print(f"🎯 下一步操作: {time_status['action']}")

        if time_status['time_to_action'] > 0:
            hours = int(time_status['time_to_action'] // 3600)
            minutes = int((time_status['time_to_action'] % 3600) // 60)
            seconds = int(time_status['time_to_action'] % 60)
            print(f"⏳ 剩余时间: {hours:02d}:{minutes:02d}:{seconds:02d}")

        print(f"📋 预约状态: {'✅ 已完成' if reserve_completed else '⏳ 待执行'}")
        print(f"🔥 秒杀状态: {'✅ 已完成' if seckill_completed else '⏳ 待执行'}")
        print(f"🔐 登录状态: {'✅ 已登录' if self.qrlogin.is_login else '❌ 未登录'}")

        try:
            if self.qrlogin.is_login and self.nick_name:
                print(f"👤 当前用户: {self.nick_name}")
        except:
            pass

        print("="*60)

    def check_and_fix_config(self):
        """检查和修复配置"""
        print("🔧 检查配置文件...")

        issues = []

        try:
            # 检查必要的配置项
            sku_id = global_config.getRaw('config', 'sku_id')
            if not sku_id or sku_id == '':
                issues.append("商品ID (sku_id) 未配置")

            buy_time = global_config.getRaw('config', 'buy_time')
            if not buy_time or buy_time == '':
                issues.append("购买时间 (buy_time) 未配置")

            eid = global_config.getRaw('config', 'eid')
            if not eid or eid == '':
                issues.append("风控参数 eid 未配置")

            fp = global_config.getRaw('config', 'fp')
            if not fp or fp == '':
                issues.append("风控参数 fp 未配置")

            # 检查时间格式
            try:
                from datetime import datetime
                datetime.strptime(buy_time, "%H:%M:%S.%f")
            except:
                issues.append("购买时间格式不正确，应为 HH:MM:SS.fff")

            if issues:
                print("❌ 发现配置问题:")
                for issue in issues:
                    print(f"   • {issue}")

                print("\n📖 配置说明:")
                print("   • sku_id: 商品ID，可从商品页面URL获取")
                print("   • buy_time: 抢购时间，格式如 09:59:59.500")
                print("   • eid/fp: 京东风控参数，需要从浏览器获取")
                print("   • 详细配置方法请参考 README.md")

                return False
            else:
                print("✅ 配置检查通过")
                return True

        except Exception as e:
            print(f"❌ 配置检查失败: {e}")
            return False

    def auto_config_wizard(self):
        """自动配置向导"""
        print("\n🧙‍♂️ 配置向导启动")
        print("="*60)

        try:
            # 检查当前配置
            if self.check_and_fix_config():
                print("✅ 当前配置完整，无需修改")
                return True

            print("\n需要完善配置，请按提示操作:")
            print("1. 打开京东商品页面")
            print("2. 获取商品ID (URL中的数字)")
            print("3. 设置抢购时间")
            print("4. 获取风控参数 (eid, fp)")
            print("\n详细步骤请参考项目文档")

            return False

        except Exception as e:
            print(f"❌ 配置向导失败: {e}")
            return False
