from .base_tests import BaseTestStaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.test import Client


class PersonalWebdriver(BaseTestStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = 'just_test'
        cls.email = 'just_test@test.com'
        cls.password = '123456saasdfasdf'
        cls.live_server_url = 'http://web:8081'
        super(PersonalWebdriver, cls).setUpClass()

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

    # @unittest.skip("demonstrating skipping")
    def test_personal_empty_default(self):
        
