# from unittest import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from pyvirtualdisplay import Display


class VisitPageWebdriver(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(VisitPageWebdriver, cls).setUpClass()
        cls.display = Display(visible=0, size=(1024, 800))
        cls.display.start()
        cls.driver = webdriver.Firefox(
            executable_path='/usr/src/app/selenium_sources/geckodriver')
        cls.driver.implicitly_wait(1)
        cls.driver.set_window_size(1024, 768)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(VisitPageWebdriver, cls).tearDownClass()

    def setUp(self):
        self.email = 'just_test@test.com'
        self.password = '123456saasdfasdf'
        self.username = 'just_test'
        active = {'is_active': 1}
        self.user_object = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                options=active,
            )

    def test_signup_success(self):
        self.driver.get(self.live_server_url + '/signup/')
        email_signup = self.driver.find_element_by_id('email_signup')
        username_signup = self.driver.find_element_by_id('username_signup')
        password_signup = self.driver.find_element_by_id('password_signup')
        signup_form = self.driver.find_element_by_class_name('signup-form')
        # the sign_up form in the middle of the screen
        self.assertAlmostEqual(
            email_signup.location['x'] + email_signup.size['width']/2,
            512, delta=25
        )
        self.assertAlmostEqual(
            username_signup.location['x'] + username_signup.size['width']/2,
            512, delta=25
        )
        self.assertAlmostEqual(
            password_signup.location['x'] + password_signup.size['width']/2,
            512, delta=25
        )
        self.assertAlmostEqual(
            signup_form.location['x'] + signup_form.size['width']/2,
            512, delta=25
        )
        # create a new user, submit the correct form
        email_signup.send_keys('just_for_test@email.com')
        username_signup.send_keys('just_for_test')
        password_signup.send_keys('just_for_password')
        self.driver.find_element_by_class_name('submit-btn').click()
        # wait for the front page show up
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')

    def test_login_success(self):
        self.driver.get(self.live_server_url + '/login/')
        email_login = self.driver.find_element_by_id('email_login')
        password_login = self.driver.find_element_by_id('password_login')
        login_form = self.driver.find_element_by_class_name('login-form')
        self.assertAlmostEqual(
            email_login.location['x'] + email_login.size['width']/2,
            512, delta=25
        )
        self.assertAlmostEqual(
            password_login.location['x'] + password_login.size['width']/2,
            512, delta=25
        )
        self.assertAlmostEqual(
            login_form.location['x'] + login_form.size['width']/2,
            512, delta=25
        )

        # submit the correct form
        email_login.send_keys('just_test@test.com')
        password_login.send_keys('123456saasdfasdf')
        self.driver.find_element_by_class_name('submit-btn').click()
        # wait for the front page show up
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')

    def tearDown(self):
        # close the browser window
        self.driver.quit()
        self.display.stop()
