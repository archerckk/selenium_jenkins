from time import sleep
from selenium import webdriver
import os
import  configparser
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_config():
    config=configparser.ConfigParser()
    if sys.platform=='win32':
        os.environ['HOMEPATH']='C:/test'
        config.read(os.path.join(os.environ['HOMEPATH'],'selenium.ini'))
    else:
        config.read(os.path.join(os.environ['HOME'],'selenium.ini'))
    print(config)
    return config

class TestWeb:


    def setup(self):
        config=get_config()
        print(config)

        try:
            using_headless= os.environ['using_headless']
        except KeyError:
            using_headless=None
            print('使用有界面模式进行测试')

        chrome_options=Options()

        if using_headless is not None and using_headless.lower()=='using_headless':
            chrome_options.add_argument('--headless')
            print('增加运行参数')

        self.driver=webdriver.Chrome(executable_path=config.get('driver','chrome_driver'),
                                     options=chrome_options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

    def teardown(self):
        self.driver.quit()

    def test_window_switch_login(self):
        '测试窗口切换模拟注册账号到登录'
        self.driver.get('https://zhidao.baidu.com/question/201422003213420205.html')
        sleep(2)

        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, "userbar-reg"))).click()
        # print(self.driver.current_window_handle)
        # print(self.driver.window_handles)
        print('填写注册资料')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.find_element_by_id('TANGRAM__PSP_4__userName').send_keys('test_user888888')
        self.driver.find_element_by_id('TANGRAM__PSP_4__phone').send_keys(13631347763)
        self.driver.find_element_by_id('TANGRAM__PSP_4__password').send_keys('test_psw')
        self.driver.switch_to.window(self.driver.window_handles[0])
        print('切换窗口')
        self.driver.find_element_by_id('userbar-login').click()
        self.driver.find_element_by_id('TANGRAM__PSP_11__footerULoginBtn').click()
        self.driver.find_element_by_id('TANGRAM__PSP_11__userName').send_keys('test_user888888')
        self.driver.find_element_by_id('TANGRAM__PSP_11__password').send_keys('test_psw')
        print(('输出账号密码登录'))
        sleep(3)
        assert self.driver.find_element_by_id('TANGRAM__PSP_11__submit')is not None

    def test_time_value(self):
        '测试用js修改12306的车票日期'
        self.driver.get('https://www.12306.cn/index/')
        self.driver.execute_script("document.getElementById('train_date').removeAttribute('readonly')")
        sleep(2)
        self.driver.execute_script("document.getElementById('train_date').value='2020-12-30'")
        sleep(2)
        print(self.driver.execute_script("return document.getElementById('train_date').value"))
        assert self.driver.execute_script("return document.getElementById('train_date').value") == '2020-12-30'
        # print(self.driver.find_element_by_id('train_date').text)
        sleep(3)