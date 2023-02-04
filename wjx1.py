import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = 'https://www.wjx.cn/vm/h4eAvAV.aspx'


# 生成m到n之间的o个不重复的数字
def int_random(m, n, o):
    p = []
    while len(p) < o:
        new_int = random.randint(m, n)
        if new_int not in p:
            p.append(new_int)
    return p


def run():
    # 躲避智能检测
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                            })
    driver.get(url)

    # 总共有28个题目
    i = 1
    while i <= 27:
        # 单选、多选xpath //*[@id="div21"]/div[2]/div[2]
        base_xpath1 = '//*[@id="div{}"]'.format(i)
        base_xpath3 = base_xpath1 + '/div[2]/div'
        # a表示所有选项的div标签
        a = driver.find_elements(By.XPATH, base_xpath3)
        # b在选项长度之内的随机数
        b = random.randint(1, len(a))

        if i <= 21:  # 单选
            # 通过随机数字，点击该数字的选项
            driver.find_element(By.CSS_SELECTOR,
                                '#div{} > div.ui-controlgroup > div:nth-child({})'.format(i, b)).click()
        # 多选题 i-->22-27
        elif i in range(22, 28):
            # 生成b个1到选项长度len(a)个随机数
            q = int_random(1, len(a), b)
            # sort函数表示将列表排序，如果未加参数表示从小到大排列
            q.sort()
            for r in q:
                driver.find_element_by_css_selector(
                    '#div{} > div.ui-controlgroup > div:nth-child({})'.format(i, r)).click()
        i += 1

    # 排序题//*[@id="div28"]/ul/li[1]
    base_xpath1 = '//*[@id="div{}"]'.format(i)
    base_xpath3 = base_xpath1 + '/ul/li'
    a = driver.find_elements(By.XPATH, base_xpath3)
    q = int_random(1, len(a), len(a))

    for r in q:
        try:
            driver.find_element_by_css_selector(
                '#div28 > ul.ui-controlgroup > li:nth-child({})'.format(r)).click()
        except:
            pass
    # 第29题
    driver.find_element_by_css_selector('#q29').send_keys('暂无')
    # ------------------------------------------------------------------------
    time.sleep(0.5)
    # 点击提交
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    # 出现点击验证码验证
    time.sleep(0.5)
    try:
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(0.5)
    except:
        print("无智能验证")
    # 关闭页面
    time.sleep(4)
    handles = driver.window_handles
    driver.switch_to.window(handles[0])

    # 关闭当前页面，如果只有一个页面，则也关闭浏览器
    driver.close()


count = 0
while True:
    run()
    count += 1
    print('已填写{}份-{}'.format(count, time.strftime('%H:%M:%S', time.localtime(time.time()))))
