import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = 'https://www.wjx.cn/vm/mBLV2Uy.aspx#'


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

    # 总共有27个题目
    i = 1
    while i <= 27:
        base_xpath1 = '//*[@id="div{}"]'.format(i)
        base_xpath3 = base_xpath1 + '/div[2]/div'
        # a表示所有选项的div标签
        a = driver.find_elements(By.XPATH, base_xpath3)
        b = random.randint(1, len(a))
        # 通过随机数字，点击该数字的选项
        driver.find_element(By.CSS_SELECTOR, '#div{} > div.ui-controlgroup > div:nth-child({})'.format(i, b)).click()

        # 4题答案为1时，剔除第5道题
        if i == 4 and b == 1:
            i = 6
        # 5题时剔除第6道题
        elif i == 5:
            i = 7
        # 当第24题答案是2时，跳到26
        elif i == 24 and b == 2:
            i = 26
        else:
            i += 1

    # 点击提交按钮
    time.sleep(0.5)
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
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    # 关闭页面
    time.sleep(4)
    handles = driver.window_handles
    driver.switch_to.window(handles[0])

    # 刷新页面（可能不需要）
    driver.refresh()
    # 关闭当前页面，如果只有一个页面，则也关闭浏览器
    driver.close()


count = 0

while True:
    run()
    count += 1
    print('已填写{}份-{}'.format(count, time.strftime('%H:%M:%S', time.localtime(time.time()))))
