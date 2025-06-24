import sys

from maotai.jd_spider_requests import JdSeckill

if __name__ == '__main__':
    a = """

       oooo oooooooooo.            .oooooo..o                     oooo         o8o  oooo  oooo
       `888 `888'   `Y8b          d8P'    `Y8                     `888         `"'  `888  `888
        888  888      888         Y88bo.       .ooooo.   .ooooo.   888  oooo  oooo   888   888
        888  888      888          `"Y8888o.  d88' `88b d88' `"Y8  888 .8P'   `888   888   888
        888  888      888 8888888      `"Y88b 888ooo888 888        888888.     888   888   888
        888  888     d88'         oo     .d8P 888    .o 888   .o8  888 `88b.   888   888   888
    .o. 88P o888bood8P'           8""88888P'  `Y8bod8P' `Y8bod8P' o888o o888o o888o o888o o888o
    `Y888P

功能列表：
 1.预约商品
 2.秒杀抢购商品
 3.全自动化执行（预约+秒杀）
    """
    print(a)

    jd_seckill = JdSeckill()

    # 进行基本的配置检查（不管是否登录）
    print("🔍 检查基本配置...")
    try:
        jd_seckill._check_basic_config()
    except SystemExit:
        # 配置检查失败，程序退出
        sys.exit(1)
    except Exception as e:
        print(f"配置检查出错: {e}")
        print("请检查配置后重新运行程序")
        sys.exit(1)

    # 如果用户已登录，进行完整的配置验证
    if jd_seckill.qrlogin.is_login:
        print("检测到用户已登录，进行完整配置验证...")
        try:
            jd_seckill._validate_and_setup_config()
        except SystemExit:
            # 配置验证失败，程序退出
            sys.exit(1)
        except Exception as e:
            print(f"配置验证出错: {e}")
            print("请检查配置后重新运行程序")
            sys.exit(1)

    # 重新显示功能列表，确保用户能看到选项
    print("\n" + "="*50)
    print("功能列表：")
    print(" 1.预约商品")
    print(" 2.秒杀抢购商品")
    print(" 3.全自动化执行（预约+秒杀）")
    print("="*50)
    choice_function = input('请选择:')
    if choice_function == '1':
        jd_seckill.reserve()
    elif choice_function == '2':
        jd_seckill.seckill_by_proc_pool()
    elif choice_function == '3':
        print("\n" + "="*60)
        print("全自动化模式启动")
        print("="*60)
        print("系统将自动执行预约和秒杀流程")
        print("无需人工干预，请保持程序运行")
        print("="*60)
        jd_seckill.auto_mode()
    else:
        print('没有此功能')
        sys.exit(1)

