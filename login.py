from selenium import webdriver
import os
import time
import json


########步骤一##########
def browser_initial():
    """"
    进行浏览器初始化
    """
    #cookie保存路径 放桌面好复制
    os.chdir('C:\\Users\\chili\\Desktop\\')
    browser = webdriver.Edge()
    # 下面的网址填登录界面的网址
    log_url = 'https://www.luogu.com.cn/auth/login'
    return log_url, browser


def get_cookies(log_url, browser):
    """
    获取cookies保存至本地
    """
    browser.get(log_url)
    time.sleep(60)  # 进行登录 等待60s 可以设置短点
    dictCookies = browser.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

    with open('damai_cookies.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')


if __name__ == "__main__":
    tur = browser_initial()
    get_cookies(tur[0], tur[1])