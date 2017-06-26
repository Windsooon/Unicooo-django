from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase
from activities.models import Act


class CreateActWebdriver(BaseTestStaticLiveServerTestCase):

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

    def test_create_act_without_title_failed(self):
        self.act_cover_image.send_keys(
            '/usr/src/app/func_tests/images/images_test.jpg')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'act-cover-btn')))
        finally:
            self.act_content.send_keys('just_test_content_tent')
            self.driver.find_element_by_id(
                'act-cover-btn').send_keys(Keys.ENTER)
            self.assert_equal_error_text(
                'act_title-error',
                'Please enter your act title.')
            self.assertEqual(Act.objects.count(), 0)

    def test_create_act_without_content_failed(self):
        self.act_cover_image.send_keys(
            '/usr/src/app/func_tests/images/images_test.jpg')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'act-cover-btn')))
        finally:
            self.act_title.send_keys('just_test_title')
            self.driver.find_element_by_id(
                'act-cover-btn').send_keys(Keys.ENTER)
            self.assert_equal_error_text(
                'act_content-error',
                'Please enter your act content.')
            self.assertEqual(Act.objects.count(), 0)

    def test_create_act_success(self):
        self.act_cover_image.send_keys(
            '/usr/src/app/func_tests/images/images_test.png')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'act-cover-btn')))
        finally:
            self.act_title.send_keys('just_test_title')
            self.act_content.send_keys('just_test_content_tent')
            self.driver.find_element_by_id(
                'act-cover-btn').send_keys(Keys.ENTER)
            self.wait_element_url(
                'activity-details-thumb',
                'class',
                url='http://web:8081/act/just_test/just_test_title/',
            )
            self.assertEqual(Act.objects.count(), 1)
