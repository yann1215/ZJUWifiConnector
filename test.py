
# Function: 测试网页SSL认证时使用的脚本
# Update: 25.03.06
# Notice:

import requests

url = "https://net2.zju.edu.cn/"

try:
    response = requests.get(url, verify=False, timeout=5)
    print(f"网站返回状态码: {response.status_code}")
except requests.exceptions.SSLError:
    print("SSL 证书错误，网站可能无法访问！")
except Exception as e:
    print(f"请求出错: {e}")
