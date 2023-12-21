import pandas as pd
import time
import random
import re
import csv
from selenium import webdriver
import json, os, time
from selenium.webdriver.chrome.options import Options
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import sys
import datetime


def make_print_to_file(path='./'):
    class Logger(object):
        def __init__(self, filename="Default.log", path="./"):
            self.terminal = sys.stdout
            self.path = os.path.join(path, filename)
            self.log = open(self.path, "a", encoding='utf8', )
            print("save:", os.path.join(self.path, filename))

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

        def flush(self):
            pass

    fileName = datetime.datetime.now().strftime('day' + '%Y_%m_%d')
    sys.stdout = Logger(fileName + '.log', path=path)
    #############################################################
    # 这里输出之后的所有的输出的print 内容即将写入日志
    #############################################################
    print(fileName.center(60, '*'))


def readinfile(path):
    df = pd.read_excel(path, header=0)
    df = df.values.tolist()  # 转化为列表
    return df


def write_to_csv(total_info):
    time_start = time.time()
    with open(r'D:/Internship/天眼查爬取/tianyancha_output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['公司名称', '法定代表人', '经营状态', '成立日期', '注册资本',
                         '天眼评分', '统一社会信用代码', '纳税人识别号', '组织机构代码',
                         '营业期限', '核准日期', '企业类型', '行业', '登记机关', '注册地址', '经营范围'])
        writer.writerows(total_info[0:])


def get_cookies(cookie_path):
    with open(cookie_path) as f:
        cookies_file = f.read()
        cookie_list = json.loads(cookies_file)
    return cookie_list


def set_option(chrome_options):
    # 设置代理
    chrome_options.add_argument("--proxy-server=http://112.194.88.136:8080")
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    chrome_options.add_argument('--disable-images')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=400,400")
    # 屏蔽webdriver特征
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.page_load_strategy = 'eager'
    return chrome_options


def copy_info(information, browser):
    establish_date_locator = (By.XPATH, '//tbody[1]/tr[2]/td[2]')
    WebDriverWait(browser, 10, 0.01).until(EC.presence_of_element_located(establish_date_locator))
    # 法人代表
    try:
        information.append(browser.find_element(By.XPATH, '//a[@class="index_avatar-name__L5eUh link-click"]').get_attribute('innerText'))
    except selenium.common.exceptions.NoSuchElementException:
        information.append('-')
    # 经营状态
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[1]/td[4]').get_attribute('innerText'))
    # 成立日期
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[2]/td[2]').get_attribute('innerText'))
    # 注册资本
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[3]/td[2]').get_attribute('innerText'))
    # 天眼评分
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[1]/td[6]/div/span[2]').get_attribute('innerText'))
    # 信用代码
    information.append(browser.find_element(By.XPATH, '//tbody/tr[5]/td[2]').get_attribute('innerText'))
    # 纳税人识别号
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[5]/td[4]').get_attribute('innerText'))
    # 组织机构代码
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[5]/td[6]').get_attribute('innerText'))
    # 营业期限
    information.append(
        browser.find_element(By.XPATH, '//tbody[1]/tr[6]/td[2]').get_attribute('innerText').replace(u'\xa0', u' '))
    # 核准日期
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[6]/td[6]').get_attribute('innerText'))
    # 企业类型
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[7]/td[2]').get_attribute('innerText'))
    # 行业
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[7]/td[4]').get_attribute('innerText'))
    # 登记机关
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[8]/td[4]').get_attribute('innerText'))
    # 注册地址
    address = browser.find_element(By.XPATH, '//td[@colspan="5"]')
    address = address.get_attribute('innerText')
    address = re.sub(r'附近公司', '', address)
    information.append(address)
    # 经营范围
    information.append(browser.find_element(By.XPATH, '//tbody[1]/tr[11]/td[2]').get_attribute('innerText'))
    return information


def getinformation(filepath):
    df = readinfile(filepath)  # 读取文件到dataframe
    total_info = []

    cookie_path = r'D:/Internship/天眼查爬取/tianyancha_cookies.txt'
    cookie_list = get_cookies(cookie_path)

    chrome_options = Options()
    chrome_options = set_option(chrome_options)
    browser = webdriver.Chrome(options=chrome_options)
    page_url = 'https://www.tianyancha.com/'
    browser.get(page_url)
    browser.delete_all_cookies()
    for cookie in cookie_list:
        browser.add_cookie(cookie)

    for i in range(60,100):
        time_start = time.time()
        information = []
        search = browser.find_elements(By.TAG_NAME, 'input')
        name = df[i][0]
        information.append(name)
        search[1].send_keys(name + Keys.ENTER)
        locator = (By.XPATH, '//a[@class="index_alink__zcia5 link-click"]')
        WebDriverWait(browser, 20, 0.01).until(EC.presence_of_element_located(locator))
        browser.find_element(By.XPATH, '//a[@class="index_alink__zcia5 link-click"]').click()
        # 切换到新窗口,并等待加载完毕
        window_handle = browser.window_handles[1]
        browser.switch_to.window(window_handle)
        establish_date_locator = (By.XPATH, '//tbody[1]/tr[2]/td[2]')
        WebDriverWait(browser, 20, 0.01).until(EC.presence_of_element_located(establish_date_locator))

        information = copy_info(information, browser)
        time.sleep(random.randint(5, 7))
        total_info.append(information)
        browser.close()
        # 切换回第一个窗口
        window_handle = browser.window_handles[0]
        browser.switch_to.window(window_handle)
        logo_locator = (By.XPATH, '//div[@class="tyc-header-container"]/a/i')
        WebDriverWait(browser, 20, 0.01).until(EC.presence_of_element_located(logo_locator))
        browser.find_element(By.XPATH, '//div[@class="tyc-header-container"]/a/i').click()
        time_end = time.time()
        time_sum = time_end - time_start
        print('%s %d / %d   \t \t %d s' % (name, i + 1, len(df), time_sum))

    return total_info


if __name__ == '__main__':
    make_print_to_file(path='./')
    filepath = 'D:\Internship\天眼查爬取\企业测试1130.xlsx'
    total_info = getinformation(filepath)
    write_to_csv(total_info)
