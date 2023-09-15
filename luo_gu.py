import re
import bs4
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys
import concurrent.futures



desktop_path = os.path.expanduser("~/Desktop")  # 桌面路径
题库文件夹 = os.path.join(desktop_path, "题库")  # 题库文件夹路径

def getMD(html):
    bs = bs4.BeautifulSoup(html,"html.parser")
    core = bs.select("article")[0]
    h1_tag = bs.find("h1")  # 查找第一个出现的<h1>标签

    if h1_tag:
        title_span = h1_tag.find("span", attrs={"title": True})  # 在<h1>标签内查找具有title属性的<span>标签
        if title_span:
            title_text = title_span.text.strip()  # 提取<span>标签内的文本并去除首尾空格
        else:
            title_text = "Unknown"
    else:
        title_text = "No <h1> tag found"
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    # 保留数学公式
    math_formulas = re.findall(r"\$(.*?)\$", md)
    for i, formula in enumerate(math_formulas):
        md = md.replace(f"${formula}$", f"__MATH_{i}__")
    # 替换 $1 \leq a \leq 20$ 这样的模式
    md = re.sub(r'\$(.*?)\$', r'`\1`', md)

    # 替换 $1 \leq x \leq n \leq 20$ 这样的模式 
    md = re.sub(r'\$(.*?)\$', r'`\1`', md)

    # 替换 $1 \leq m \leq 2 \times 10^4$ 这样的模式
    md = re.sub(r'\$(.*?)\$', r'`\1`', md)
    md = re.sub(r'\\leq', r'≤', md)
    md = re.sub(r'\\times', r'×', md)

    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)

    # 恢复数学公式
    for i, formula in enumerate(math_formulas):
        md = md.replace(f"__MATH_{i}__", formula)

    # 去除公式中的 $ 符号
    md = re.sub(r"\$(.*?)\$", r"\1", md)
    return md


# 基础URL和递增后缀的起始值和结束值
base_url = "https://www.luogu.com.cn/problem/P%s"  # 基础URL，%s将被替换为后缀

start_suffix = 1000
end_suffix = 1050  # 递增后缀的结束值

# 反爬机制
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
session = requests.Session()
session.headers.update(headers)

def get_topic(url,suffix):
    # 发起请求获取网页内容,,这个地方试了好久的静态爬取，最后原来是要加headers啊🤣
    response = requests.get(url, timeout=30, headers=headers)
    html_content = response.text

    # 解析网页
    markdown_text = getMD(html_content)

    # print (markdown_text)

    soup = BeautifulSoup(html_content, "html.parser")
    
    #获取题目
    core = soup.select("article")[0]
    title = soup.select("h1")

    题目编号 = "P" + str(suffix)
    Title = title[0].string

    # print(title) 测试了一下

    # 创建文件夹路径
    文件夹路径 = os.path.join(题库文件夹, f"{题目编号}-{Title}")  # 题目文件夹路径
    
    # 检查文件夹是否存在
    if os.path.exists(文件夹路径):
        # 删除已存在的文件夹内的所有文件
        for file_name in os.listdir(文件夹路径):
            file_path = os.path.join(文件夹路径, file_name)
            os.remove(file_path)
    else:
        # 创建空的题目文件夹
        os.makedirs(文件夹路径)
    # 创建并写入Markdown文件
    文件名 = f"{题目编号}-{Title}.md"
    文件路径 = os.path.join(文件夹路径, 文件名)
    with open(文件路径, "w", encoding="utf-8") as file:
        file.write(markdown_text)
        print("P"+str(suffix)+ " "+title[0].string + " 题目成功爬取")
        sys.stdout.flush()


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # 使用多线程并发爬取多个页面
        for suffix in range(start_suffix, end_suffix + 1):
            # 构建当前网页的URL
            url = base_url % suffix
            executor.submit(get_topic, url, suffix)
