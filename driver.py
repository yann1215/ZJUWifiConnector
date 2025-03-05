
# Function: 自动更新EdgeDriver的版本，使之与Edge浏览器版本匹配
# Update: 25.03.05
# Notice: 删减了程序的功能
#       自定义driver安装路径不利于打包（太难了），所以放弃了安装在main同一文件夹的操作
#       目前按照webdriver_manager的默认设置，driver安装在C盘
#       且受限于权限，不进行zip的删除，有需要的话可以根据路径手动删除安装压缩包


from webdriver_manager.microsoft import EdgeChromiumDriverManager


def update_driver():

    # 自动下载匹配版本的 EdgeDriver
    print("———— 检查EdgeDriver版本")
    driver_path = None
    try:
        # 下载并安装 EdgeDriver
        driver_path = EdgeChromiumDriverManager().install()
        print("EdgeDriver安装路径:", driver_path)
        print("EdgeDriver版本已是最新")
        return driver_path, True
    except Exception as e:
        print(f"EdgeDriver下载失败: {e}")
        # print("请检查网络配置后重新运行程序")
        return driver_path, False


if __name__ == "__main__":
    update_driver()