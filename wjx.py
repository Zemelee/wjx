import random
import time

import numpy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

"""
readme:
    代码使用规则：
        你需要提前安装python环境，且已具备上述的所有安装包（笔者的selenium版本号：3.141.0，版本号是3就可以，其余安装包默认即可）
        还需要下载好chrome的webDriver自动化工具，并将其放在python安装目录下，以便和selenium配套使用（详情请自行百度）
    效果展示:
            http://b23.tv/7o1TW83
    使用教程：
            http://b23.tv/T7hWEES
    代码原理:
        通过html标签定位到每一道题，再按指定概率点击每道题的选项
    注意：
        这份代码目前只做示范，仅仅针对下面url中的链接有效，如果需要刷自己的问卷，需要自己修改run函数和url变量
        后续会添加代理功能，以实现提交ip的指定，敬请期待（划掉）
        ip代理、多窗口同时填写、同一窗口重复填写（效率更高，更省CPU）、翻页、更多题型已经实现，代码付费。
    最后的最后：
        如果对代码有任何疑问，欢迎在平台（不是指github）上私我，我看到后会尽快给出解答
        代码可能具有时效性，但短时间内暂时还不会失效
        如果不会python但确有需要，欢迎在平台私我
"""

#
# 用户测试的问卷，不会暂停，可放心填写提交
url = 'https://www.wjx.cn/vm/QaaZ20B.aspx#'
# 数据查看链接，密码：1234
# https://www.wjx.cn/wjx/activitystat/verifyreportpassword.aspx?viewtype=1&activity=209176245&type=1

# 生成滑动轨迹
tracks = [i for i in range(1, 50, 3)]


# 生成m到n之间的o个不重复的数字列表，用于多选题
# m指1,n指多选题的选项个数，o为小于n大于等于1的随机数
def int_random(m, n, o):
    p = []
    while len(p) < o:
        new_int = random.randint(m, n)
        if new_int not in p:
            p.append(new_int)
    return p


def run():
    # 躲避智能检测，将网页的window.navigator中的webdriver设置为false
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                            })
    # 设置浏览器的大小和位置
    driver.set_window_size(600, 500)
    driver.set_window_position(x=400, y=50)
    # 访问问卷链接
    driver.get(url)

    # 第1题单选
    i = 1  # 通过xpath定位到第i题的所有选项
    xpath = '//*[@id="div{}"]'.format(i) + '/div[2]/div'  # 每一道题的div
    a = driver.find_elements(By.XPATH, xpath)
    # 生成1到选项个数之间的随机数
    b = random.randint(1, len(a))
    driver.find_element(By.CSS_SELECTOR,  # 通过selector定位选项的某个子元素
                        '#div{} > div.ui-controlgroup > div:nth-child({})'.format(i, b)).click()

    # 第2题多选题
    i = 2
    xpath = '//*[@id="div{}"]'.format(i) + '/div[2]/div'  # 每一道题的div组成的列表
    a = driver.find_elements(By.XPATH, xpath)
    b = random.randint(1, len(a))
    # 生成1到选项个数之间的随机数
    q = int_random(1, len(a), b)
    q.sort()  # sort函数表示将列表排序，如果未加参数表示从小到大排列
    for r in q:
        driver.find_element_by_css_selector(
            '#div{} > div.ui-controlgroup > div:nth-child({})'.format(i, r)).click()

    # 第3题矩阵题
    i = 3
    for j in range(1, 7):  # 矩阵题有6个选择题
        # 指定2-6的概率分布
        r = numpy.random.choice(a=numpy.arange(2, 7), p=[0.27, 0.35, 0.13, 0.2, 0.05])
        # r = random.randint(2, 6)  # 每个选择题5个选项生成随机数
        driver.find_element(By.CSS_SELECTOR, '#drv{}_{} > td:nth-child({})'.format(i, j, r)).click()

    # 第4题滑动题、填空题
    score = random.randint(1, 100)
    driver.find_element(By.CSS_SELECTOR, '#q4').send_keys(score)

    # 第5题填空题
    list = ["1", "2", "3"]
    index = random.randint(0, 2)
    # 随机填写1，2，3
    driver.find_element(By.CSS_SELECTOR, '#q5').send_keys(list[index])

    # 第6题排序题
    i = 6
    xpath = '//*[@id="div{}"]'.format(i) + '/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    for j in range(1, len(a) + 1):
        b = random.randint(j, 4)
        driver.find_element(By.CSS_SELECTOR, '#div{} > ul > li:nth-child({})'.format(i, b)).click()
        time.sleep(0.4)
    # ------------------------------------------------------------------------

    # 点击提交
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    # 出现点击验证码验证
    time.sleep(1)
    # 点击对话框的确认按钮
    driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]').click()
    time.sleep(0.5)
    # 点击智能检测按钮
    driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
    time.sleep(4)
    # 滑块验证
    try:
        # 定位滑块
        slider = driver.find_element(By.XPATH,
                                     '/html/body/div[1]/form/div[7]/div[8]/div[2]/div/div/div/div[3]/div[1]/div/div[1]/span')
        # 模拟鼠标按住不放
        ActionChains(driver).click_and_hold(slider).perform()
        # 按滑动轨迹移动
        try:
            for x in tracks:
                # 按轨迹沿x方向滑动
                ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
                time.sleep(0.01)
        except:
            #  模拟释放鼠标
            ActionChains(driver).release().perform()
    except:
        pass
    # 关闭页面
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    # 关闭当前页面，如果只有一个页面，则也关闭浏览器
    driver.close()


count = 0
while True:
    run()
    count += 1
    print('已填写{}份-{}'.format(count, time.strftime('%H:%M:%S', time.localtime(time.time()))))
