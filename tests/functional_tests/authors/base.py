from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_browser
import time
from selenium.webdriver.common.by import By

class AuthorBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_browser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, seconds=5):
        time.sleep(seconds)
    
    def get_by_placeholder(self, webelement, placeholder):
        return webelement.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
    
    