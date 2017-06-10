from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BaseTestStaticLiveServerTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Remote(
            command_executor='http://zalenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)
        cls.brower_size = cls.driver.get_window_size()
        cls.live_server_url = 'http://web:8081'
        cls.login_required_url = cls.live_server_url + '/act/new/'
        super(BaseTestStaticLiveServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(BaseTestStaticLiveServerTestCase, cls).tearDownClass()

    def assert_equal_error_text(self, ident, text, element='id'):
        if element == 'id':
            wrapper = self.driver.find_element_by_id(ident)
        elif element == 'class':
            wrapper = self.driver.find_element_by_class_name(ident)
        self.assertEqual(
            wrapper.text, text)

    def send_to_element(self, ident, text, element='id'):
        if element == 'id':
            wrapper = self.driver.find_element_by_id(ident)
        elif element == 'class':
            wrapper = self.driver.find_element_by_class_name(ident)
        wrapper.send_keys(text)

    def check_user_authed(self):
        self.driver.get(self.login_required_url)
        self.assertEqual(
            self.driver.current_url, self.login_required_url)

    def wait_element_url(self, ident, element='id', url=None, timeout=6):
        try:
            if element == 'id':
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.ID, ident))
                )
            elif element == 'class':
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, ident))
                )
        finally:
            self.assertEqual(
                self.driver.current_url,
                self.live_server_url + '/' if not url else url)

    def wait_element_text(
            self, ident, text, element='id', url=None, timeout=6):
        try:
            if element == 'id':
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.ID, ident))
                )
            elif element == 'class':
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, ident))
                )
        finally:
            self.assert_equal_error_text(ident, text, element)
