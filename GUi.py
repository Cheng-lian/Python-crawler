import os
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import tkinter.font as tkfont



def crawl_problems():
    subprocess.call(['python', 'luo_gu.py'])

def crawl_solutions():
    subprocess.call(['python', 'luo_gu_t.py'])

def crawl_tag():
    subprocess.call(['python', 'tag.py'])

# 标志变量，用于跟踪代码的运行状态
is_crawling_problems = False
is_crawling_solutions = False


def main():
    class ClickableText(tk.Text):
        def __init__(self, master=None, **kwargs):
            super().__init__(master, **kwargs)
            self.tag_configure("clickable", foreground="blue", underline=True)
            self.tag_bind("clickable", "<Button-1>", self.on_click)
        
        def on_click(self, event):
            index = self.tag_closest("current")
            folder_name = self.get(index + " linestart", index + " lineend")
            folder_path = os.path.join(r"C:\Users\chili\Desktop\题库", folder_name)
            os.startfile(folder_path)
    
    #标签检索
    def find_folders_with_keyword(folder_path, filter):
        matching_folders = []

        # 获取题库文件夹下的所有文件夹
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

        # 遍历文件夹并检查是否包含关键字文件
        for folder in folders:
            folder_contents = os.listdir(os.path.join(folder_path, folder))
            if any(f"{filter}.txt" in content for content in folder_contents):
                matching_folders.append(folder)

        return matching_folders
    
    # 对筛选的复用
    def display_folders_with_keyword(keyword):
        
        # 将斜杠替换为连字符(因为window不支持带/的文件名，所以我稍作修改)
        keyword = keyword.replace('/', '−')
        
        # 清空文本框中的内容
        output_text.delete("1.0", tk.END)
        folder_path = r"C:\Users\chili\Desktop\题库"  # 替换为实际的题库文件夹路径
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

        # 在文本框中显示包含指定关键字的文件夹名称
        for folder in folders:
            if f"{keyword}.txt" in os.listdir(os.path.join(folder_path, folder)):
                output_text.insert(tk.END, folder + "\n", "clickable")
                output_text.tag_add("clickable", "insert linestart", "insert lineend")
    
    # 配置文本框的标签样式和绑定点击事件
    def open_folder(event):
        folder_name = event.widget.get("current linestart", "current lineend")
        folder_path = os.path.join(r"C:\Users\chili\Desktop\题库", folder_name)
        os.startfile(folder_path)
    
    # 各种界面值
    def update_selected_filters(*args):
        # 清空文本框中的内容
        output_text.delete("1.0", tk.END)
        
        filter_value = filter_select.get()
        keyword_value = keyword_input.get()
        content_search_value = content_search.get()

        selected_filters = []

        #筛选条件
        if filter_value:
            selected_filters.append(f"筛选条件：{filter_value}")
        
        # 根据筛选条件调用不同的显示函数
        if filter_value and keyword_value == '':
            display_folders_with_keyword(filter_value)
        
        #关键词
        if keyword_value:
            selected_filters.append(f"关键字：{keyword_value}")
            if(filter_value==''):
                # 遍历题库文件夹路径下的所有文件夹
                folder_path = r"C:\Users\chili\Desktop\题库"  # 替换为实际的题库文件夹路径
                folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

                # 在文本框中显示匹配的文件夹名称
                for folder in folders:
                    if keyword_value in folder:
                        output_text.insert(tk.END, folder + "\n","clickable")
                        output_text.tag_add("clickable", "insert linestart", "insert lineend")
                    if f"{keyword_value}.txt" in os.listdir(os.path.join(folder_path, folder)):
                        output_text.insert(tk.END, folder + "\n", "clickable")
                        output_text.tag_add("clickable", "insert linestart", "insert lineend")

            else:
                # 清空文本框中的内容
                output_text.delete("1.0", tk.END)

                # 根据筛选条件筛选文件夹
                folder_path = r"C:\Users\chili\Desktop\题库"  # 替换为实际的题库文件夹路径
                folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
                # 将斜杠替换为连字符(因为window不支持带/的文件名，所以我稍作修改)
                filter_value = filter_value.replace('/', '−')
                matching_folders = find_folders_with_keyword(folder_path, filter_value)
                # 在文本框中显示匹配的文件夹名称
                for folder in matching_folders:
                    if keyword_value in folder:
                        output_text.insert(tk.END, folder + "\n","clickable")
                        output_text.tag_add("clickable", "insert linestart", "insert lineend")
                    elif f"{keyword_value}.txt" in os.listdir(os.path.join(folder_path, folder)):
                        output_text.insert(tk.END, folder + "\n", "clickable")
                        output_text.tag_add("clickable", "insert linestart", "insert lineend")
        
        if content_search_value:
            selected_filters.append("搜索题目内容")

        selected_filters_text.set(
            ", ".join(selected_filters)
            if selected_filters
            else "暂无，可在上方进行多维度筛选，例如：普及-（难度）、CSP-J（来源）、2020（时间）、动态规划（算法）"
        )

    def start_luo_gu():
        process = subprocess.Popen(['python', 'luo_gu.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,encoding='utf-8')
        # 实时更新luo_gu脚本的输出到GUI界面
        for line in iter(process.stdout.readline, ''):
            output_text.insert(tk.END, line)  # 将输出逐行插入到文本框中
            output_text.see(tk.END)  # 滚动到文本框底部，显示最新的输出
            window.update()  # 更新GUI界面
        process.stdout.close()
        process.wait()
        # 爬取完成后恢复正常状态
        window.after(0, restore_button_state)

    def start_luo_gu_t():
        process = subprocess.Popen(['python', 'luo_gu_t.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,encoding='utf-8')
        # 实时更新luo_gu脚本的输出到GUI界面
        for line in iter(process.stdout.readline, ''):
            output_text.insert(tk.END, line)  # 将输出逐行插入到文本框中
            output_text.see(tk.END)  # 滚动到文本框底部，显示最新的输出
            window.update()  # 更新GUI界面
        process.stdout.close()
        process.wait()
        # 爬取完成后恢复正常状态
        window.after(0, restore_solution_state)

    def start_tag():
        process = subprocess.Popen(['python', 'tag.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,encoding='utf-8')
        # 实时更新luo_gu脚本的输出到GUI界面
        for line in iter(process.stdout.readline, ''):
            output_text.insert(tk.END, line)  # 将输出逐行插入到文本框中
            output_text.see(tk.END)  # 滚动到文本框底部，显示最新的输出
            window.update()  # 更新GUI界面
        process.stdout.close()
        process.wait()
        # 爬取完成后恢复正常状态
        window.after(0, restore_tag_state)

    def crawl_button_clicked():
        crawl_problems_button.config(state=tk.DISABLED)  # 禁用 "爬取" 按钮
        # crawl_problems_button_style.configure('CrawlButton.TButton', background='red')  # 设置按钮的背景颜色为红色
        status_label.config(foreground='red')  # 将标签的文本颜色设置为红色
        status_label_var.set("正在爬取...")
        # status_label.pack(side=tk.LEFT)  # 将状态标签放置在按钮的右侧
        window.update()  # 更新 GUI 界面，使状态标签立即显示
        threading.Thread(target=start_luo_gu).start()  # 在后台线程中运行爬取操作
        # 在crawl_button_clicked函数执行完成后，立即执行crawl_tag_clicked函数
        # window.update()
        """ # 爬取完成后恢复正常状态
        status_label.pack_forget()  # 隐藏状态标签
        status_label_var.set("")  # 清空状态标签的文本 """
    
    # 爬取完成后恢复正常状态(题目的)
    def restore_button_state():
        status_label.config(foreground='black')  # 将标签的文本颜色设置为黑色
        status_label_var.set("爬取完成")
        crawl_problems_button.config(state=tk.NORMAL)  # 恢复按钮的状态
        # crawl_problems_button_style.configure('CrawlButton.TButton', background='SystemButtonFace')  # 恢复按钮的背景颜色
        window.update()  # 更新 GUI 界面
    
    def crawl_solutions_clicked():
        crawl_solutions_button.config(state=tk.DISABLED)  # 禁用 "爬取" 按钮,并将背景改为红色
        status_label.config(foreground='red')  # 将标签的文本颜色设置为红色
        status_label_var.set("正在爬取...")
        # status_label.pack(side=tk.LEFT)  # 将状态标签放置在按钮的右侧
        window.update()  # 更新 GUI 界面，使状态标签立即显示

        threading.Thread(target=start_luo_gu_t).start()  # 在后台线程中运行爬取操作

        """ # 爬取完成后恢复正常状态
        status_label.pack_forget()  # 隐藏状态标签
        status_label_var.set("")  # 清空状态标签的文本 """
    
    # 爬取完成后恢复正常状态
    def restore_solution_state():
        status_label.config(foreground='black')  # 将标签的文本颜色设置为黑色
        status_label_var.set("爬取完成")
        crawl_solutions_button.config(state=tk.NORMAL)
        #crawl_problems_button.config(state=tk.NORMAL, bg='SystemButtonFace')  # 恢复 "爬取" 按钮的正常状态和背景颜色
        window.update() # 更新 GUI 界面

    def crawl_tag_clicked():
        crawl_tag_button.config(state=tk.DISABLED)  # 禁用 "爬取" 按钮,并将背景改为红色
        status_label.config(foreground='red')  # 将标签的文本颜色设置为红色
        status_label_var.set("正在爬取...")
        # status_label.pack(side=tk.LEFT)  # 将状态标签放置在按钮的右侧
        window.update()  # 更新 GUI 界面，使状态标签立即显示

        threading.Thread(target=start_tag).start()
    
    def restore_tag_state():
        status_label.config(foreground='black')  # 将标签的文本颜色设置为黑色
        status_label_var.set("爬取完成")
        crawl_tag_button.config(state=tk.NORMAL)
        #crawl_problems_button.config(state=tk.NORMAL, bg='SystemButtonFace')  # 恢复 "爬取" 按钮的正常状态和背景颜色
        # 更新 GUI 界面
        window.update() 
    
    # 创建窗口
    window = tk.Tk()
    window.title("搜索引擎")

    # 设置主窗口背景颜色
    window.configure(bg="#E0E0E0")  
    
    # 使用clam主题
    style = ttk.Style()
    style.theme_use("clam")  
    style.configure('My.TButton', background='#4CAF50', foreground='white')
    
    # 正在爬取
    status_label_var = tk.StringVar()
    status_label = tk.Label(window, textvariable=status_label_var)
    status_label.pack()
    
    # 创建容器框架
    container = ttk.Frame(window)
    container.pack(padx=10, pady=10)
    my_button = ttk.Button(container, text="爬取洛谷题目", style='My.TButton')
    # GUI界面下面的输出框
    output_text = tk.Text(window) 
    output_text.pack()

    #设置字体样式
    font = tkfont.Font(family="Arial", size=12)
    output_text.configure(font=font)

    # 配置文本框的标签样式和绑定点击事件
    output_text.tag_configure("clickable", foreground="blue", underline=True)
    output_text.tag_bind("clickable", "<Button-1>", open_folder)

    # 设置文本框中字体样式
    font = tkfont.Font(family="黑体", size=12)
    output_text.configure(font=font)

    # 禁用文本框的编辑功能
    output_text.config(state=tk.NORMAL)
    # 配置文本框为只读
    output_text.configure(inactiveselectbackground=output_text.cget("selectbackground"))
    output_text.bind("<Key>", lambda e: "break")
    
    # 创建样式对象
    crawl_problems_button_style = ttk.Style()
    # 定义按钮的样式
    crawl_problems_button_style.configure('CrawlButton.TButton', background='SystemButtonFace')

    # 题目按钮
    crawl_problems_button = ttk.Button(container, text="爬取洛谷题目", command=crawl_button_clicked)
    crawl_problems_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # 题解按钮
    crawl_solutions_button = ttk.Button(container, text="爬取洛谷题解", command=crawl_solutions_clicked)
    crawl_solutions_button.grid(row=2, column=5, padx=5, pady=5, sticky="w")

    # 标签按钮
    crawl_tag_button = ttk.Button(container, text="爬取标签", command=crawl_tag_clicked)
    crawl_tag_button.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    # 添加标题
    title_label = ttk.Label(container, text="所属题库")
    title_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    # 添加选项按钮
    luogu_button = ttk.Button(container, text="洛谷")
    luogu_button.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    theme_button = ttk.Button(container, text="主题库")
    theme_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    entry_buttons = [
        ttk.Button(container, text="入门与面试"),
        ttk.Button(container, text="CodeForces"),
        ttk.Button(container, text="SPOJ"),
        ttk.Button(container, text="AtCoder"),
        ttk.Button(container, text="UVA"),
    ]

    for i, button in enumerate(entry_buttons):
        button.grid(row=4, column=i+2, padx=5, pady=5, sticky="w")

    # 添加筛选条件部分
    filter_section = ttk.Frame(container)
    filter_section.grid(row=5, column=0, columnspan=6, padx=5, pady=5, sticky="w")

    filter_label = ttk.Label(filter_section, text="筛选条件：")
    filter_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    filter_select = ttk.Combobox(filter_section, values=["暂无评定", "入门", "普及−", "普及/提高−", "普及+/提高", "提高+/省选−", "NOI/NOI+/CTSC"])
    filter_select.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    filter_select.bind("<<ComboboxSelected>>", update_selected_filters)

    keyword_label = ttk.Label(filter_section, text="关键词：")
    keyword_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")

    keyword_input = ttk.Entry(filter_section)
    keyword_input.grid(row=3, column=3, padx=5, pady=5, sticky="w")
    keyword_input.bind("<KeyRelease>", update_selected_filters)

    content_search = tk.BooleanVar()
    content_search_check = ttk.Checkbutton(filter_section, text="搜索题目内容", variable=content_search, command=update_selected_filters)
    content_search_check.grid(row=3, column=4, padx=5, pady=5, sticky="w")

    # 添加搜索按钮
    search_button = ttk.Button(container, text="搜索")
    search_button.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    # 添加已选择的筛选条件
    selected_filters_text = tk.StringVar()
    selected_filters_label = ttk.Label(container, text="已选择：")
    selected_filters_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")

    selected_filters_display = ttk.Label(container, textvariable=selected_filters_text, foreground="#C0C0C0")
    selected_filters_display.grid(row=7, column=1, columnspan=5, padx=5, pady=5, sticky="w")

    # 运行程序
    window.mainloop()

if __name__ == "__main__":
    main()