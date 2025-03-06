from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
import os

ROOT_DIR = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_DIR / 'bin' / CHROMEDRIVER_NAME
CHROME_BIN = "/home/marcos/chrome/linux-133.0.6943.126/chrome-linux64/chrome"

def make_browser(*options):
    chrome_options = Options()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')
    chrome_options.binary_location = CHROME_BIN
    service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

if __name__ == '__main__':
    browser = make_browser('--headless', '--no-sandbox')
    browser.get('http://www.udemy.com')
    sleep(5)    
    browser.quit()
