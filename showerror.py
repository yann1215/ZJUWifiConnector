
# Function: 放了一个简单的“报错，结束程序执行并退出”的函数
# Update: 25.03.01
# Notice:

import sys

def show_error(e):
    print(f"发生错误: {e}")
    sys.exit(1)