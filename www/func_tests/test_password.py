from django.contrib.auth import get_user_model
from django.test import Client
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_tests import BaseTestStaticLiveServerTestCase


class Passworddriver(BaseTestStaticLiveServerTestCase):

    def setUp(self):
        self.email = 'just_test@test.com'
        self.password = '123456saasdfasdf'
        self.username = 'just_test'
        self.user_object = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                is_active=1
            )
        self.client = Client()
        self.client.force_login(self.user_object)
        self.cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/act/new/')
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': self.cookie.value,
            'secure': False, 'path': '/'})

    def tearDown(self):
        pass

    def test_change_password_exist(self):
        self.driver.get(
            self.live_server_url + '/' + self.username + '/settings/')
        try:
            WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((
                    By.CLASS_NAME, "settings-form"))
            )
        finally:
            self.driver.find_element_by_id("change-btn").click()
            self.wait_element_url(
                "password-form", "class",
                self.live_server_url + '/change_password/')

    def test_change_password_empty_failed(self):
        self.driver.get(
            self.live_server_url + '/change_password/')
        self.driver.find_element_by_id(
            "password-btn").send_keys(Keys.ENTER)
        self.assert_equal_error_text(
            'id_old_password-error',
            'Please enter your old password.')
        self.assert_equal_error_text(
            'id_new_password1-error',
            'Please enter your new password.')
        self.assert_equal_error_text(
            'id_new_password2-error',
            'Please enter your new password again.')

    def test_wrong_old_password_failed(self):
        self.driver.get(
            self.live_server_url + '/change_password/')
        self.driver.find_element_by_id(
            'id_old_password').send_keys('1111111111')
        self.driver.find_element_by_id(
            'password-btn').send_keys(Keys.ENTER)
        self.assert_equal_error_text(
            'id_old_password-error',
            'Your old password is incorrect.')

    def test_new_password_not_match_failed(self):
        self.driver.get(
            self.live_server_url + '/change_password/')
        self.driver.find_element_by_id(
            'id_old_password').send_keys('1111111111')
        self.driver.find_element_by_id(
            'id_new_password1').send_keys('1111111111')
        self.driver.find_element_by_id(
            'id_new_password2').send_keys('222222222')
        self.driver.find_element_by_id(
            'password-btn').send_keys(Keys.ENTER)
        self.assert_equal_error_text(
            'id_new_password2-error',
            'Password doesn\'t match the confirmation.')
        self.assert_equal_error_text(
            'id_new_password1-error',
            'Password doesn\'t match the confirmation.')

    def test_new_password_successed(self):
        self.driver.get(
            self.live_server_url + '/change_password/')
        self.driver.find_element_by_id(
            'id_old_password').send_keys(self.password)
        self.driver.find_element_by_id(
            'id_new_password1').send_keys('222222222')
        self.driver.find_element_by_id(
            'id_new_password2').send_keys('222222222')
        self.driver.find_element_by_id(
            'password-btn').send_keys(Keys.ENTER)
        self.wait_element_text('success-span', 'SUCCESS', 'class')
