from selenium import webdriver
import json, os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# 选择保存目录
outdir = r'D:\Internship\天眼查爬取'
# 登录的网址
url = 'https://www.tianyancha.com/'
chrome_options = Options()
chrome_options.add_argument("--proxy-server=http://112.194.88.136:8080")
# 启动浏览器
driver = webdriver.Chrome(options=chrome_options)
# 浏览器打开网页
driver.get(url)
time.sleep(20)
# 浏览器登录后获取cookie
cookies = driver.get_cookies()
# 将cookies保存在本地
with open(os.path.join(outdir, './tianyancha_cookies.txt'), mode='w') as f:
    f.write(json.dumps(cookies))
# 关闭浏览器
driver.close()