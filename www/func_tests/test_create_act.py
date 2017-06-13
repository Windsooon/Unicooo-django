import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase


class CreateActWebdriver(BaseTestStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.email = 'just_test@test.com'
        cls.password = '123456saasdfasdf'
        cls.username = 'just_test'
        super(CreateActWebdriver, cls).setUpClass()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                is_active=1
            )
        self.client = Client()
        self.client.force_login(self.user)
        self.cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/act/new/')
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': self.cookie.value,
            'secure': False, 'path': '/'})
        self.driver.get(self.live_server_url + '/act/new/')
        self.act_title = self.driver.find_element_by_id('act_title')
        self.act_content = self.driver.find_element_by_id('act_content')
        self.act_cover_image = self.driver.find_element_by_id(
            'act-cover-image')
        self.act_cover_span = self.driver.find_element_by_id(
            'act-cover-span')
        self.act_cover_btn = self.driver.find_element_by_id('act-cover-btn')

    def tearDown(self):
        pass

    def test_create_act_success(self):
        self.act_cover_span.click()
        self.act_cover_span.send_keys(Keys.CANCEL)
        time.sleep(2)
        self.act_cover_image.send_keys(
            '/usr/src/app/func_tests/images/images_test.png')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "act-cover-btn")))
        finally:
            self.act_title.send_keys('just_test_title')
            self.act_content.send_keys('just_test_content_tent')
            self.act_cover_btn.click()
        self.wait_element_url("front-matrix")
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_create_act_without_title_failed(self):
        self.act_cover_image.send_keys(
            '/usr/src/app/func_tests/images/images_test.jpg')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "act-cover-btn")))
        finally:
            self.act_content.send_keys('just_test_content_tent')
            self.act_cover_btn.click()
            self.assert_equal_error_text(
                'act_title-error',
                'Please enter your act title.')
            self.assertEqual(get_user_model().objects.count(), 0)

    def test_create_act_without_content_failed(self):
        self.act_cover_image.send_keys(
            '/usr/src/app/func_tests/images/images_test.jpg')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "act-cover-btn")))
        finally:
            self.act_title.send_keys('just_test_title')
            self.act_cover_btn.click()
            self.assert_equal_error_text(
                'act_title-error',
                'Please enter your act title.')
            self.assertEqual(get_user_model().objects.count(), 0)
