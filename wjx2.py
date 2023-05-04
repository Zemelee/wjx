import random
import re
from threading import Thread
import time

import numpy
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


# 获取代理ip
def getips(num):
    ips = []
    api = f"http://http.tiqu.alibabaapi.com/getip?num={num}&type=3&pack=117495&port=1&lb=2&pb=4&regions="
    ip_and_port = requests.get(api).text  # 获取ip和端口
    pattern = r"(\d+\.\d+\.\d+\.\d+):(\d+)"
    matches = re.findall(pattern, ip_and_port)
    for match in matches:
        ip = match[0]
        port = match[1]
        dist = {"ip": ip, "port": port}
        ips.append(dist)
    return ips


# 获取一个代理ip
# ips = []
ips = getips(1)
print("代理ip池：", ips)
# --------------------------------------------

url = 'https://www.wjx.cn/vm/OM6GYNV.aspx#'  # 100-40

# 单选题概率参数，"1"表示第一题，100表示必选，0表示不选， [30, 70]表示3:7
single_prob = {"1": [1, 1, 0], "2": -1, "3": -1, "4": -1, "5": -1, "6": [1, 0], }

# 下拉框参数
droplist_prob = {"1": [1, 1, 1]}

# 多选题概率参数,0不选该题，[0]不选该选项，100必选，10, 50表示1:5,-1表示随机 4个选项 在没有比选的情况下 1-2  5个选项-选4个
multiple_prob = {"9": [100, 2, 1, 1]}
# 多选题数量参数，去除必选后的数
multiple_opts = {"9": 1, }

# 矩阵题概率参数,-1表示随机
matrix_prob = {"1": [100, 0, 0, 0, 0], "2": -1, "3": [100, 0, 0, 0, 0], "4": [100, 0, 0, 0, 0],
               "5": [100, 0, 0, 0, 0], "6": [100, 0, 0, 0, 0]}

# 量表题概率参数
scale_prob = {"7": [0, 2, 3, 4, 1], "12": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10]}

# 填空题内容
texts = {"8": ["提升自己", "积累经验", " 认可"]}
# 每个内容对应的概率0:1:1:0，0表示跳过不填
texts_prob = {"8": [1, 1, 1]}

# 参数归一化
for prob in [single_prob, matrix_prob, droplist_prob, scale_prob, texts_prob]:
    for key in prob:
        if isinstance(prob[key], list) and prob[key] != -1:
            prob_sum = sum(prob[key])
            prob[key] = [x / prob_sum for x in prob[key]]

# 转化为列表
single_prob = list(single_prob.values())
droplist_prob = list(droplist_prob.values())
multiple_prob = list(multiple_prob.values())
multiple_opts = list(multiple_opts.values())
matrix_prob = list(matrix_prob.values())
scale_prob = list(scale_prob.values())
texts_prob = list(texts_prob.values())
texts = list(texts.values())

print("单选题参数：", single_prob)
print("下拉框参数：", droplist_prob)
print("多选题参数：", multiple_prob)
print("矩阵题参数：", matrix_prob)
print("量表题参数：", scale_prob)


# 检测题量和页数的函数[]
def detect(driver):
    q_list = []  # 长度等于页数，数字代表该页的题数
    xpath = '//*[@id="divQuestion"]/fieldset'
    page_num = len(driver.find_elements(By.XPATH, xpath))  # 页数
    qs = driver.find_elements(By.XPATH, f'//*[@id="fieldset1"]/div')  # 每一页的题
    invalid_item = 0  # 无效问题数量
    # 遍历每一个“题”，判断其是否可以回答
    for qs_item in qs:
        # 判断其topic属性值是否值包含数字
        if qs_item.get_attribute("topic").isdigit() is False:
            invalid_item += 1
    # 如果只有1页
    q_list.append(len(qs) - invalid_item)
    if page_num >= 2:
        for i in range(2, page_num + 1):
            qs = driver.find_elements(By.XPATH, f'//*[@id="fieldset{i}"]/div')
            # 遍历每一个“题”，判断其是否可以回答
            for qs_item in qs:
                # 判断其topic属性值是否值包含数字
                if qs_item.get_attribute("topic").isdigit() is False:
                    invalid_item += 1
            q_list.append(len(qs) - 1)
    return q_list


def vacant(driver, current, index):
    content = texts[index]
    # 对应填空题概率参数
    p = texts_prob[index]
    text_index = numpy.random.choice(a=numpy.arange(0, len(p)), p=p)
    driver.find_element(By.CSS_SELECTOR, f'#q{current}').send_keys(content[text_index])


def single(driver, current, index):
    #         //*[@id="div1"]/div[2]/div
    xpath = f'//*[@id="div{current}"]/div[2]/div'
    a = driver.find_elements(By.XPATH, xpath)
    p = single_prob[index]
    if p == -1:
        r = random.randint(1, len(a))
    else:
        r = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=p)  # [0.5, 0.5, 0]
    driver.find_element(By.CSS_SELECTOR,
                        f'#div{current} > div.ui-controlgroup > div:nth-child({r})').click()


def droplist(driver, current, index):
    # 先点击“请选择”
    driver.find_element(By.CSS_SELECTOR, f"#select2-q{current}-container").click()
    time.sleep(0.5)
    # 选项数量
    options = driver.find_elements(By.XPATH, f"//*[@id='select2-q{current}-results']/li")
    p = droplist_prob[index]  # 对应概率
    r = numpy.random.choice(a=numpy.arange(1, len(options)), p=p)
    driver.find_element(By.XPATH, f"//*[@id='select2-q{current}-results']/li[{r + 1}]").click()


def multiple(driver, current, index):
    xpath = f'//*[@id="div{current}"]/div[2]/div'
    options = driver.find_elements(By.XPATH, xpath)
    # 第current题对应的概率值
    probabilities = multiple_prob[index]
    if probabilities == 0:  # 不选
        return
    elif probabilities == -1:  # 随机
        r = random.randint(1, len(options))
        driver.find_element(By.CSS_SELECTOR,
                            f'#div{current} > div.ui-controlgroup > div:nth-child({r})').click()
    else:
        prob_copy = probabilities.copy()
        opts_num = multiple_opts[index]  # 第current题对应的选项数量参数
        for i in prob_copy:  # 如果存在列表中概率为100的项，则直接选择该项
            if i == 100:
                # 找到100元素位置
                sure = prob_copy.index(i)
                driver.find_element(By.CSS_SELECTOR,
                                    f'#div{current} > div.ui-controlgroup > div:nth-child({sure + 1})').click()
                # 将已选的概率修改为0，以便在后面按概率选择其他选项
                prob_copy[sure] = 0
        # 计算不为0的数值总和
        total = sum([num for num in prob_copy])
        if total == 0: return
        # 将不为0的数值归一化
        probabilities_norm = [num / total if num != 0 else 0 for num in prob_copy]
        # 从位置1到列表长度之间随机选择 opts_num - 已选数 相同数量的选项
        selection_indices = numpy.random.choice(
            range(len(options)),
            size=opts_num,
            replace=False,
            p=probabilities_norm)
        # 选择随机选择的选项
        for i in selection_indices:
            driver.find_element(By.CSS_SELECTOR,
                                f'#div{current} > div.ui-controlgroup > div:nth-child({i + 1})').click()


def matrix(driver, current, index):
    xpath1 = f'//*[@id="divRefTab{current}"]/tbody/tr'
    a = driver.find_elements(By.XPATH, xpath1)
    q_num = 0  # 矩阵的题数量
    for tr in a:
        if tr.get_attribute("rowindex") is not None:
            q_num += 1
    # 选项数量
    xpath2 = f'//*[@id="drv{current}_1"]/td'
    b = driver.find_elements(By.XPATH, xpath2)  # 题的选项数量+1 = 6
    # 遍历每一道小题
    for i in range(1, q_num + 1):
        p = matrix_prob[index]
        index += 1
        if p == -1:
            opt = random.randint(2, len(b))
        else:
            opt = numpy.random.choice(a=numpy.arange(2, len(b) + 1), p=p)
        driver.find_element(By.CSS_SELECTOR, f'#drv{current}_{i} > td:nth-child({opt})').click()
    return index


def reorder(driver, current):
    xpath = f'//*[@id="div{current}"]/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    for j in range(1, len(a) + 1):
        b = random.randint(j, len(a))
        driver.find_element(By.CSS_SELECTOR, f'#div{current} > ul > li:nth-child({b})').click()
        time.sleep(0.4)


def scale(driver, current, index):
    xpath = f'//*[@id="div{current}"]/div[2]/div/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    p = scale_prob[index]
    if p == -1:
        b = random.randint(1, len(a))
    else:
        b = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=p)
    driver.find_element(By.CSS_SELECTOR,
                        f"#div{current} > div.scale-div > div > ul > li:nth-child({b})").click()


# 刷题逻辑函数
def brush(driver):
    q_list = detect(driver)
    single_num = 0  # 第num个单选题
    vacant_num = 0  # 第num个多选题
    droplist_num = 0  # 第num个多选题
    multiple_num = 0  # 第num个多选题
    matrix_num = 0  # 第num个矩阵小题
    scale_num = 0  # 第num个量表题
    current = 0  # 题号
    for j in q_list:  # 遍历每一页
        for k in range(1, j + 1):  # 遍历该页的每一题
            current += 1
            # 判断题型
            q_type = driver.find_element(By.CSS_SELECTOR, f'#div{current}').get_attribute("type")
            if q_type == "1" or q_type == "2":  # 填空题
                vacant(driver, current, vacant_num)
                vacant_num += 1
            elif q_type == "3":  # 单选
                single(driver, current, single_num)
                single_num += 1
            elif q_type == "4":  # 多选
                multiple(driver, current, multiple_num)
                multiple_num += 1
            elif q_type == "5":  # 量表题
                scale(driver, current, scale_num)
                scale_num += 1
            elif q_type == "6":  # 矩阵题
                matrix_num = matrix(driver, current, matrix_num)
            elif q_type == "7":  # 下拉框
                droplist(driver, current, droplist_num)
                droplist_num += 1
            elif q_type == "8":  # 滑块题
                score = random.randint(1, 100)
                driver.find_element(By.CSS_SELECTOR, f'#q{current}').send_keys(score)
            elif q_type == "11":  # 排序题
                reorder(driver, current)
            else:
                print(f"第{k}题为不支持题型！")
        time.sleep(0.5)
        #  一页结束过后要么点击下一页，要么点击提交
        try:
            driver.find_element(By.CSS_SELECTOR, '#divNext').click()  # 点击下一页
            time.sleep(0.5)
        except:
            # 点击提交
            driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    submit(driver)


# 提交函数
def submit(driver):
    try:
        # 出现点击验证码验证
        time.sleep(1)
        # 点击对话框的确认按钮
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
        # 点击智能检测按钮
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(3)
    except:
        print("无验证")
    # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
    except:
        pass


# 反复执行brush函数的函数
def run(xx, yy):
    # 躲避智能检测，将webDriver设置为false
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    # 随机获取某个代理值
    if len(ips) == 0:
        pass
    else:
        r = random.randint(0, len(ips) - 1)
        current_ip = ips[r]["ip"]
        current_port = ips[r]["port"]
        option.add_argument(f'--proxy-server={current_ip}:{current_port}')
    driver = webdriver.Chrome(options=option)
    driver.set_window_size(600, 400)
    driver.set_window_position(x=xx, y=yy)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                            })
    while True:
        global count
        driver.get(url)
        url1 = driver.current_url
        brush(driver)
        time.sleep(4)
        url2 = driver.current_url
        if url1 != url2:
            count += 1
            print(f"已填写{count}份 - {time.strftime('%H:%M:%S', time.localtime(time.time()))}")
            driver.get(url)
        else:
            # 再等2秒
            time.sleep(2)


# 多线程执行run函数
if __name__ == "__main__":
    count = 0
    thread_1 = Thread(target=run, args=(50, 50))
    thread_1.start()
    # thread_2 = Thread(target=run, args=(650, 280))
    # thread_2.start()
    thread_3 = Thread(target=run, args=(650, 50))
    thread_3.start()
