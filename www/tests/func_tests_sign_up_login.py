from django.test import TestCase
from selenium import webdriver


class visitPageWebdriver(TestCase):
    def setUp(self):
        # create a new Firefox session
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        # navigate to the application home page

    def test_search_box(self):
        # check search box exists on Home page
        pass
        self.driver.get("http://127.0.0.1/login/")
        email_input = self.driver.find_element_by_id('email_login')

    def tearDown(self):
        # close the browser window
        self.driver.quit()
