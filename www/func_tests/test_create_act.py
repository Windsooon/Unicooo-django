from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        active = {'is_active': 1}
        cls.user = get_user_model().objects.create_user(
                username=cls.username,
                email=cls.email,
                password=cls.password,
                options=active,
            )
        # cls.client = Client()
        # cls.client.force_login(cls.user)
        # cls.client.get('/')
        # cls.cookie = cls.client.cookies['sessionid']
        super(CreateActWebdriver, cls).setUpClass()

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/act/new/')
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': self.cookie.value,
            'secure': False, 'path': '/'})
        self.driver.get(self.live_server_url + '/act/new/')

    def tearDown(self):
        pass

    def test_create_act_success(self):
        act_cover_image = self.driver.find_element_by_id('act-cover-image')
        act_cover_btn = self.driver.find_element_by_id('act-cover-btn')
        act_cover_image.send_keys(
            '/usr/src/app/func_tests/images/images_test.png')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "act-cover-btn")))
        finally:
            act_cover_btn.click()
        self.wait_element_url("front-matrix")
