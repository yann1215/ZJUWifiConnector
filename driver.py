
# Function: 自动更新EdgeDriver的版本，使之与Edge浏览器版本匹配
# Update: 25.03.05
# Notice: 考虑到大部分人都是Windows系统、自带Edge浏览器，但是不是所有人都有Chrome，所有用Edge浏览器的自动化


from webdriver_manager.microsoft import EdgeChromiumDriverManager

import os
import sys


def delete_zip(driver_download_path):

    # 获取所有平台的驱动包路径
    platform_path = os.path.join(driver_download_path, ".wdm", "drivers", "edgedriver")
    # print("EdgeDriver安装路径：", platform_path)

    for dir_path, dir_names, file_names in os.walk(platform_path):
        for file_name in file_names:
            if file_name.endswith('.zip'):
                    zip_file = os.path.join(dir_path, file_name)
                    try:
                        os.remove(zip_file)  # 删除压缩包
                        print("删除安装压缩包: ", file_name)
                    except Exception as e:
                        print(f"删除安装压缩包失败: {e}")


def update_driver():
    # 自定义下载路径
    os.environ["WDM_LOCAL"] = "true"  # 启用本地缓存
    # 将driver安装在同一目录下
    driver_download_path = os.getcwd()
    os.environ["WDM_CACHE_PATH"] = driver_download_path
    # print("当前目录：", driver_download_path)

    # 自动下载匹配版本的 EdgeDriver
    print("———— 检查EdgeDriver版本")
    try:
        # 下载并安装 EdgeDriver
        driver_path = EdgeChromiumDriverManager().install()
        print("EdgeDriver版本已是最新")
    except Exception as e:
        print(f"EdgeDriver下载失败: {e}")
        print("请检查网络配置后重新运行程序")
        sys.exit(1)  # 终止程序运行

    # 清除目录内的压缩包
    delete_zip(driver_download_path)

    # 返回driver地址（文件名）
    return driver_path

if __name__ == "__main__":
    update_driver()