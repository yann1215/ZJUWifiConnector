
# Function: 自动更新EdgeDriver的版本，使之与Edge浏览器版本匹配
# Update: 25.03.06
# Notice: 删减了程序的功能；增加了无网络情况下可登录的选项
#       自定义driver安装路径不利于打包（太难了），所以放弃了安装在main同一文件夹的操作
#       目前按照webdriver_manager的默认设置，driver安装在C盘
#       且受限于权限，不进行zip的删除，有需要的话可以根据路径手动删除安装压缩包


from webdriver_manager.microsoft import EdgeChromiumDriverManager
from shutil import copy as copy_file

import sys
import os

def update_driver():
    # 自动下载匹配版本的 EdgeDriver
    print("———— 检查EdgeDriver版本")

    if getattr(sys, 'frozen', False):
        # 打包成EXE时，使用 sys._MEIPASS 作为基础目录
        base_dir = sys._MEIPASS
    else:
        # 未打包时，使用脚本所在目录作为基础目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path_copy = os.path.join(base_dir, "msedgedriver.exe")

    try:
        # 下载并安装 EdgeDriver
        driver_path = EdgeChromiumDriverManager().install()
        print("EdgeDriver安装路径:", driver_path)
        print("EdgeDriver版本已是最新")

        # 备份driver.exe，防止未联网的时候无法使用
        copy_file(driver_path, driver_path_copy)

        return driver_path, True
    except Exception as e:
        print(f"EdgeDriver下载失败: {e}")
        if os.path.exists(driver_path_copy):
            driver_path = driver_path_copy
        else:
            driver_path = None
        # print("path:", driver_path)
        return driver_path, False


if __name__ == "__main__":
    update_driver()