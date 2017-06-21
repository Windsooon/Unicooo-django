from django.contrib.auth import get_user_model
from django.test import Client
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from .base_tests import BaseTestStaticLiveServerTestCase


class SettingsWebdriver(BaseTestStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = 'just_test'
        cls.email = 'just_test@test.com'
        cls.password = '123456saasdfasdf'
        cls.live_server_url = 'http://web:8081'
        super(SettingsWebdriver, cls).setUpClass()

    def setUp(self):
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

    def test_set_details_settings(self):
        self.driver.get(
            self.live_server_url + '/' + self.username + '/settings/')
        details = self.driver.find_element_by_id('user-details')
        details.send_keys('just_for_test_details')
        settings_btn = self.driver.find_element_by_id('setting-btn')
        settings_btn.send_keys(Keys.ENTER)
        self.wait_element_text('success-span', 'SUCCESS', 'class')
        self.driver.get(
            self.live_server_url + '/' + self.username + '/settings/')

        new_details = self.driver.find_element_by_id(
            'user-details').get_attribute('value')
        self.assertEqual('just_for_test_details', new_details)

    def test_set_gender_settings(self):
        self.driver.get(
            self.live_server_url + '/' + self.username + '/settings/')
        details = self.driver.find_element_by_id('user-details')
        details.send_keys('just_for_test_details')
        element = Select(self.driver.find_element_by_id('id_user_gender'))
        for i in element.options:
            if i.text == 'MAIE':
                i.click()
        settings_btn = self.driver.find_element_by_id('setting-btn')
        settings_btn.send_keys(Keys.ENTER)
        self.wait_element_text('success-span', 'SUCCESS', 'class')
        self.driver.get(
            self.live_server_url + '/' + self.username + '/settings/')
        gender = self.driver.find_element_by_id('id_user_gender')
        self.assertEqual(gender.text, 'MAIE')
