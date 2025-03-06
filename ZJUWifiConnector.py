
# Function: 打开Edge浏览器，打开网址，进行登录
# Update: 25.03.06
# Notice: 考虑到大部分人都是Windows系统、自带Edge浏览器，但是不是所有人都有Chrome，所有用Edge浏览器的自动化
#       1. 打包了Edge Driver，这下初次无网络也能正常启动了（但是还要录入用户名和密码）
#       2. 显示QQBrowser user data path not found 问题无法解决，就让它显示吧（悲）
#       3. 程序延时关闭的功能改为在.bat文件中实现


import time
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from driver import update_driver
from error import show_error


# ============ User Data Manager ==========
def save_user_data(user_data_file, username, password):
    with open(user_data_file, "w") as file:
        file.write(f"{username}\n{password}\n")  # 将用户名和密码保存到文件中


def load_user_data(user_data_file):
    if os.path.exists(user_data_file):  # 检查文件是否存在
        with open(user_data_file, "r") as file:
            username = file.readline().strip()  # 读取用户名
            password = file.readline().strip()  # 读取密码
            return username, password
    return None, None  # 如果文件不存在，返回 None


# ================ Status Check =================
def login_success_check(driver):
    try:
        # 寻找主界面内容
        # 通过登录后界面的用户个人信息图标，判断是否登录成功
        driver.find_element(By.ID, "logout-dm")
        return True
    except NoSuchElementException:
        return False


# Wrong Account
def wrong_userdata_check(driver):
    print("进行登录状态检测")
    try:
        error_element = driver.find_element(By.XPATH, "//div[@type='dialog']")
        error_info_list = error_element.text.split("\n")
        error_info = error_info_list[1]
        print("登录失败:", error_info)
        try:
            cancel_button = driver.find_element(By.CLASS_NAME, "layui-layer-btn0")
            cancel_button.click()
            time.sleep(1)
            # print("检测到登录异常")
            return True # 发生了错误
        except NoSuchElementException as e:
            driver.quit()
            show_error(e)
    except NoSuchElementException:
        # print("未检测到登录异常")
        return False


# ================ Input User Data =================
def input_userdata(driver, username, password):
    # —————————— 输入用户名 ——————————
    try:
        # 找到用户名输入框
        username_input_container = driver.find_element(By.ID, "username")
        # 清空输入框，防止重复输入
        username_input_container.clear()
        # 输入用户名
        username_input_container.send_keys(username)
    except NoSuchElementException as e:
        driver.quit()
        show_error(e)

    # ——————————— 输入密码 ——————————
    try:
        # 找到密码输入框
        password_input_container = driver.find_element(By.ID, "password")
        # 清空输入框，防止重复输入
        password_input_container.clear()
        # 输入密码
        password_input_container.send_keys(password)
    except NoSuchElementException as e:
        driver.quit()
        show_error(e)

    # ——————————— 进行登录 ——————————
    try:
        login_button = driver.find_element(By.ID, "login")
        login_button.click()
    except NoSuchElementException as e:
        driver.quit()
        show_error(e)
    return


# ================ Main Function =================
def login(driver_path):

    # ———————————————— Information ————————————————
    # 目标登录页面 URL
    url = "https://net2.zju.edu.cn/"  # 替换成你要登录的网址

    if getattr(sys, 'frozen', False):
        # 打包成EXE时，使用 sys._MEIPASS 作为基础目录
        base_dir = sys._MEIPASS
    else:
        # 未打包时，使用脚本所在目录作为基础目录
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # 登录信息
    user_data_file = os.path.join(base_dir, "user_data.txt")
    username, password = load_user_data(user_data_file)
    if not username or not password:
        print("未能找到用户信息，需要录入用户名和密码")
        username = input("请输入用户名: ")
        while not username:
            username = input("用户名不能为空，请输入用户名: ")
        password = input("请输入密码: ")
        while not password:
            password = input("密码不能为空，请输入密码: ")
        save_user_data(user_data_file, username, password)
    else:
        print("用户信息已导入")

    # —————————————— Launch Driver ———————————————

    # 创建 Edge 选项对象
    driver_options = Options()
    driver_options.add_argument("--headless")  # 开启无头模式
    driver_options.add_argument("--disable-gpu")  # 兼容某些系统上的问题

    driver_options.use_chromium = True  # 确保使用 Chromium 内核的 Edge
    driver_options.add_argument("--no-sandbox")  # 禁用沙盒模式

    # 规避 Selenium 检测（可以解决SSL报错的问题）
    driver_options.add_argument("--disable-blink-features=AutomationControlled")
    driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 禁用日志
    # 禁用SSL验证
    driver_options.add_argument("--ignore-certificate-errors")
    driver_options.add_argument("--ignore-ssl-errors")
    # 允许不安全的SSL证书
    driver_options.add_argument("--allow-running-insecure-content")

    # # 解决显示
    # driver_options.add_argument("--no-default-browser-check")
    # driver_options.add_argument("--disable-background-mode")
    # driver_options.add_argument("--disable-extensions")  # 禁用所有扩展

    # 启动浏览器驱动
    driver_service = Service(
        executable_path=driver_path,
        # log_output=open(os.devnull, 'w'),   # 将Edge日志输出定向到空设备
    )
    driver = webdriver.Edge(options=driver_options, service=driver_service)
    print("\n———— 启动Edge浏览器")

    try:
        driver.get(url)
        # 等待页面加载
        time.sleep(1)
    except WebDriverException as e:
        show_error(e)

    # 检测是否需要进行登录操作
    # 如果直接进入主界面，就不需要进行登录
    if login_success_check(driver):
        print("网络认证已登录")
        driver.quit()
        return

    # ——————————————— Password Check ———————————————
    # 检测密码是否输入正确
    # 登录失败时，尝试重新输入密码3次
    # 如果重新输入密码3次之后，还是不成功，就重新输入用户名与密码、让用户重启程序
    password_attempt = 4

    while True:
        print("尝试登录...")
        input_userdata(driver, username, password)
        time.sleep(1)

        error_flag = wrong_userdata_check(driver)
        if not error_flag:
            if login_success_check(driver):
                print("网络认证登录成功")
                driver.quit()
            break

        # 等待较短时间，检验是否登录失败（用户名或密码错误）
        if password_attempt:
            # 如果还有尝试次数
            print("可尝试登录次数：", password_attempt)
            username = input("请输入用户名: ")
            while not username:
                username = input("用户名不能为空，请输入用户名: ")
            password = input("请输入密码: ")
            while not password:
                password = input("密码不能为空，请输入密码: ")
            save_user_data(user_data_file, username, password)
            password_attempt -= 1

        else:
            # 如果没有尝试次数
            # print("登录失败，用户名或密码错误")
            username = input("请输入用户名: ")
            password = input("请输入密码: ")
            save_user_data(user_data_file, username, password)

            print("———— 信息已更新，请重启程序")
            driver.quit()
            input()
            sys.exit(1)

    # ——————————— Enter Verification Code ——————————
    # 校园网5次输错密码后会要求输入验证码，但是用代码处理太复杂了
    # 还是让用户自己手操一下比较快（真的会有人输错5次密码吗……？）
    # enter_verification_code(driver)
    # time.sleep(1)

    return


def auto_connect():
    print("\n欢迎使用ZJUWifiConnector!")

    # 适配 EXE 运行环境
    if getattr(sys, 'frozen', False):
        os.environ["APPDATA"] = os.path.expanduser("~\\AppData\\Roaming")
        os.environ["LOCALAPPDATA"] = os.path.expanduser("~\\AppData\\Local")

    # 先尝试对driver进行更新；如果更新不了，则尝试进行先使用已有路径进行登录
    driver_path, update_driver_flag = update_driver()
    # 如果未成功获取到已有的driver、且未能更新driver
    if not driver_path:
        print("未找到EdgeDriver: 请连接网络后重新运行程序，或在默认路径手动安装EdgeDriver")
        input()
        sys.exit(1)

    login(driver_path)

    # 如果先前未联网、未成功更新driver，则补更新一次driver
    # 保证driver版本最新
    if not update_driver_flag:
        update_driver()

    # print("\n程序运行结束，将在5秒后关闭")
    # # 保留5s界面，使用户能看到窗口最后的返回信息
    # time.sleep(5)

    return


if __name__ == "__main__":
    auto_connect()
    # input("程序运行结束，按回车键关闭程序")
