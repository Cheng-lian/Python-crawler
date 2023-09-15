from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys
import time
import requests
from bs4 import BeautifulSoup

# 创建一个 Microsoft Edge WebDriver 实例
driver = webdriver.Edge()

base_url = "https://www.luogu.com.cn/problem/P%s"
start_suffix = 1000
end_suffix = 1050  # 假设你要爬取从1000到1050的链接



""" <h1 data-v-2dfcfd35="" class="lfe-h1"><span data-v-1fbfa3c2="" data-v-2dfcfd35="" title="P1000 超级玛丽游戏">
    P1000 超级玛丽游戏
  </span></h1> """

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
# 定义一个函数用于爬取页面内容
def scrape_page(url, suffix):
        driver.get(url)
        driver.implicitly_wait(30)
        driver.minimize_window()
        elements = driver.find_elements(By.XPATH, '//a[@class="color-none"]//span')
        
        response = requests.get(url, timeout=30, headers=headers)
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")
        
        #获取题目
        core = soup.select("article")[0]
        title = soup.select("h1")

        题目编号 = "P" + str(suffix)
        Title = title[0].string
        
        for element in elements:
            span_text = element.text
            # 过滤掉不需要的文本
            if span_text not in ["题库", "题单", "比赛", "讨论","发源于"]:
                # 去除前后空白字符
                span_text = span_text.strip()
                
                if span_text:  # 检查是否为空文本
                    # 构建保存的文件路径
                    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                    folder_path = os.path.join(desktop_path, "题库",f"{题目编号}-{Title}")
                    # 移除斜杠字符
                    raw_file_name = span_text.replace("/", "−")
                    file_name = f"{raw_file_name}.txt"
                    file_path = os.path.join(folder_path, file_name)
                    
                    # 创建文件夹，如果不存在的话
                    os.makedirs(folder_path, exist_ok=True)
                    
                    # 使用文件路径打开文件，并将文本内容写入文件中
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(span_text)
        # 使用 find_element 找到需要点击的元素（假设这里是一个<a>元素）
        element_to_click = driver.find_element(By.XPATH, '//div[@class="expand-tip lfe-caption"]')

        # 模拟点击该元素
        element_to_click.click()
        # 使用 find_element 找到 class="tags-wrap multiline" 的 <div> 元素
        div_element = driver.find_element(By.XPATH, '//div[@class="tags-wrap multiline"]')
        time.sleep(1)
        # 在该 <div> 元素内部使用 find_elements 找到所有 class="tag color-none" 的 <a> 元素
        elements = div_element.find_elements(By.XPATH, './/a[@class="tag color-none"]')

        # 遍历每个 <a> 元素，然后找到其中的 <span> 元素的内容
        for element in elements:
            span_element = element.find_element(By.XPATH, './/span')  # 注意这里使用 . 表示在当前元素下查找
            span_text = span_element.text
            if span_text:  # 检查是否为空文本
                    # 构建保存的文件路径
                    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                    folder_path = os.path.join(desktop_path, "题库",f"{题目编号}-{Title}")
                    file_name = f"{span_text}.txt"
                    file_path = os.path.join(folder_path, file_name)
                    
                    # 创建文件夹，如果不存在的话
                    os.makedirs(folder_path, exist_ok=True)
                    
                    # 使用文件路径打开文件，并将文本内容写入文件中
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(span_text)
        if elements:
            print(f"{题目编号}-{Title}"+"标签已捕获") 
            sys.stdout.flush()

                

for suffix in range(start_suffix, end_suffix + 1):
    # 构建当前网页的URL
    url = base_url % suffix
    scrape_page(url, suffix)

# 关闭浏览器
driver.quit()