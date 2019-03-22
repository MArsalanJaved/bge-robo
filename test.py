from selenium import webdriver
import time
 
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--test-type")
# options.binary_location = "/usr/share/doc/google-chrome-stable"
# driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

driver.get('https://python.org')
