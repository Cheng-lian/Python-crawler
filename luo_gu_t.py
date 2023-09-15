from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys


T_base_url = "https://www.luogu.com.cn/problem/solution/P%s"
start_suffix = 1000
end_suffix = 1050  # 递增后缀的结束值 
content_list = []

url = 'https://www.luogu.com.cn/auth/login'# 

def save_to_markdown(content_list, output_file):
    markdown_text = ''
    for content in content_list:
        if content['type'] == 'text':
            markdown_text += '<p>' + content['text'] + '</p>\n\n'
        elif content['type'] == 'code':
            markdown_text += '```' + content['code'] + '\n```\n\n'

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_text)


driver = webdriver.Edge()

# 打开登录界面
driver.get(url)

cookies = [{"domain": "www.luogu.com.cn", "expiry": 1694758777, "httpOnly": False, "name": "C3VK", "path": "/", "sameSite": "Lax", "secure": False, "value": "1b8662"}, {"domain": ".luogu.com.cn", "expiry": 1697350479, "httpOnly": True, "name": "_uid", "path": "/", "sameSite": "None", "secure": True, "value": "561385"}, {"domain": ".luogu.com.cn", "expiry": 1697350458, "httpOnly": True, "name": "__client_id", "path": "/", "sameSite": "None", "secure": True, "value": "300eec9d83bfef93216d7374ce3b51dd2a3719c0"}]

for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('https:/www.luogu.com.cn')
driver.minimize_window()

for suffix in range(start_suffix, end_suffix + 1):
    # 构建当前网页的URL
    T_url = T_base_url % suffix
    
    # 反爬机制
    headers = {
        #"Cookie":"client_id=98cfc2cc86d451827cf762d426dc1b5e5551a763; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000; _uid=561385",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    driver.get(T_url)
    
    # 将以下代码进行修改
    div_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.marked')))

    # 修改循环以处理单个 div_element
    children = div_element.find_elements(By.XPATH, './*')

    # 初始化文本内容和代码内容
    text_content = ''
    code_content = ''

    # <h1 data-v-2dfcfd35 class="lfe-h1">P1000 超级玛丽游戏 题解</h1>
    # 遍历子元素，将<pre>部分作为代码段，其他部分作为文本
    for child in children:
        if child.tag_name == 'p':
            text_content = child.text + '\n'
            content_list.append({'type': 'text', 'text': '<p>' + text_content.strip() + '</p>'})
        else:
            code_content = child.text + '\n'
            content_list.append({'type': 'code', 'language': 'cpp', 'code': code_content.strip()})

    
    # 查找class为"lfe-h1"的h1元素
    h1_element = driver.find_element(By.XPATH, "//h1[@class='lfe-h1']")

    # 获取文本内容
    text_content = h1_element.text

    # 找到第一个和最后一个空格的位置
    first_space_index = text_content.index(" ")
    last_space_index = text_content.rindex(" ")

    # 替换第一个和最后一个空格为连字符
    text_content = text_content[:first_space_index] + "-" + text_content[first_space_index + 1:last_space_index] + "-" + text_content[last_space_index + 1:]
    
    filename = text_content

    #将所有"-"变成【空格】
    text_content = text_content.replace("-", " ")

    # 在第一个空格前添加连字符
    parts = text_content.split(" ", 1)  # 将文本按照第一个空格分割为两部分
    text_content = "-".join(parts)  # 将两部分用连字符连接起来    
    
    #  print(text_content)

    # 去掉最后三个字符（-题解）
    text_content = text_content[:-3]
    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, "题库", f"{text_content}")
    output_file = os.path.join(folder_path, filename + ".md")
    print(filename,"题解爬取成功")
    save_to_markdown(content_list, output_file)
    sys.stdout.flush()

# 关闭 WebDriver
driver.quit()