import random  # 内置函数写前面
import time  

import numpy as np  # 第三方库写中间
from selenium import webdriver  # 按照字母顺序依次import，e.g., selenium的s在numpy的n之后
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from src.utils import int_random, tracks  #  自己的文件写最后


class AutoQuestionnaireAnswer():
    def __init__(self, cfg) -> None:
        # 将浏览器中webDriver设置为false，以躲避智能检测
        self.cfg = cfg  # 获取配置文件
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_experimental_option('useAutomationExtension', False)
    
    def _get_total_num_choices(self, que_id, suffix='/div[2]/div'):
        """根据题号获取该题的总选项数目。

        Args:
            que_id(Int): 每一题的题号

        Returns:
            total_num_choices(Int): 该题的总选项数目
        """
        xpath = '//*[@id="div{}"]'.format(que_id) + suffix  # 每一道题的div
        xpath_ele = self.driver.find_elements(By.XPATH, xpath)
        return len(xpath_ele)
    
    # 单选题
    def single_choice_question(self, data_dict):
        que_id = data_dict['que_id']
        psbty = data_dict.get('possibility', None)
        total_num_choices = self._get_total_num_choices(que_id)
        if psbty is not None:
            assert len(psbty) == total_num_choices
            assert sum(psbty) == 1
            
        # 生成1到待选项个数之间的随机数
        selected = np.random.choice(np.arange(1, total_num_choices + 1), p=psbty)
        self.driver.find_element(By.CSS_SELECTOR,  # 通过selector定位选项的某个子元素
                            '#div{} > div.ui-controlgroup > div:nth-child({})'.format(que_id, selected)).click()
    
    # 多选题
    def multiple_choice_question(self, data_dict):
        que_id = data_dict['que_id']
        psbty = data_dict.get('possibility', None)
        total_num_choices = self._get_total_num_choices(que_id)
        # 生成1到选项个数之间的随机数
        if psbty is not None:
            assert len(psbty) == total_num_choices
            assert sum(psbty) == 1
        num_to_select = random.randint(1, total_num_choices)
        selected = np.random.choice(np.arange(1, total_num_choices + 1), num_to_select, 
                                    p=psbty, replace=False)
        for r in selected:
            self.driver.find_element_by_css_selector(
                '#div{} > div.ui-controlgroup > div:nth-child({})'.format(que_id, r)).click()

    # 矩阵题
    def matrix_question(self, data_dict):
        que_id = data_dict['que_id']
        num_row = data_dict['num_row']
        num_column = data_dict['num_column']
        psbty = data_dict.get('possibility', None)
        if psbty is not None:
            assert len(psbty) == num_row, "length of possibility must be equal to num_row"
            for each_row_psbty in psbty:
                assert len(each_row_psbty) == num_column
                assert sum(each_row_psbty) == 1, "possibility must be equal to 1"
        for j in range(1, num_row + 1):
            r = np.random.choice(a=np.arange(2, num_column + 2), p=psbty[j-1])
            self.driver.find_element(
                By.CSS_SELECTOR, '#drv{}_{} > td:nth-child({})'.format(que_id, j, r)).click()
    
    # 滑动题
    def sliding_question(self, data_dict):
        score = random.randint(1, 100)
        self.driver.find_element(By.CSS_SELECTOR, '#q4').send_keys(score)
    
    # 填空题
    def filling_blank_question(self, data_dict):
        candidate_ans = data_dict['candidate_ans']
        psbty = data_dict.get('possibility', None)
        if psbty is not None:
            assert sum(psbty) == 1
        ans = np.random.choice(candidate_ans, p=psbty)
        self.driver.find_element(By.CSS_SELECTOR, '#q5').send_keys(ans)
    
    # 排序题
    def sorting_question(self, data_dict):
        que_id = data_dict['que_id']
        total_num_choice = self._get_total_num_choices(que_id, '/ul/li')
        psbty = data_dict.get('possibility', None)
        if psbty is not None:
            assert sum(psbty) == 1
            assert len(psbty) == total_num_choice
        sorted_ans = np.random.choice(np.arange(1, total_num_choice + 1), total_num_choice, p=psbty, replace=False).tolist()
        while len(sorted_ans):
            b = sorted_ans.pop(0)
            temp = []
            for i in sorted_ans:
                aped_val = i + 1 if i < b else i
                temp.append(aped_val)
            sorted_ans = temp
            self.driver.find_element(
                By.CSS_SELECTOR, '#div{} > ul > li:nth-child({})'.format(que_id, b)).click()
            time.sleep(0.4)
    
    # 预处理：将浏览器中webDriver设置为false，以躲避智能检测
    def pre_process(self):
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get(self.cfg.URL)
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                            })

    # 后处理：如滑窗验证等
    def post_process(self):
        # time.sleep()
        # 点击提交
        self.driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
        # 出现点击验证码验证
        time.sleep(1)
        # 点击对话框的确认按钮
        self.driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]').click()
        time.sleep(0.5)
        # 点击智能检测按钮
        self.driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(4)
        # 滑块验证暂时可能会报错
        try:
            # 定位滑块
            slider = self.driver.find_element(By.XPATH,
                                        '/html/body/div[1]/form/div[7]/div[8]/div[2]/div/div/div/div[3]/div[1]/div/div[1]/span')
            # 模拟鼠标按住不放
            ActionChains(self.driver).click_and_hold(slider).perform()
            # 按滑动轨迹移动
            for x in tracks:
                ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.01)
            ActionChains(self.driver).release().perform()
        except:
            pass
        # 关闭页面
        time.sleep(6)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])
        # 关闭当前页面，如果只有一个页面，则也关闭浏览器
        self.driver.close()
    
    def run(self):
        # 预处理
        self.pre_process()

        # 根据config，依次回答每一道题
        for que_id, que_args in self.cfg.ALL_QUESTIONS.items():
            que_args.update({'que_id': int(que_id)})
            self.__getattribute__(que_args.type)(que_args)  
        
        # 后处理
        self.post_process()
