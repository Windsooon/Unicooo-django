from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase


class FrontPageWebdriver(BaseTestStaticLiveServerTestCase):

    def setUp(self):
        self.user_object = get_user_model().objects.create_user(
                username='just_test_frontpage',
                email='just_test@frontpage.com',
                password='6666666',
                is_active=1
            )
        self.client = Client()
        self.client.force_login(self.user_object)
        self.cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/')
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': self.cookie.value,
            'secure': False, 'path': '/'})

    def test_click_create_activity(self):
        '''
        click to create activity
        '''
        self.driver.find_element_by_class_name('front-btn').click()
        self.wait_element_url(
            "inter-create-act",
            url=self.live_server_url + '/act/new/'
        )

    def test_click_add_create_activity(self):
        '''
        click to create activity
        '''
        self.driver.find_element_by_id('add-btn').click()
        self.wait_element_url(
            "inter-create-act",
            url=self.live_server_url + '/act/new/'
        )

    def test_click_add(self):
        '''
        click to create activity
        '''
        self.driver.find_element_by_id('explort-btn').click()
        self.wait_element_url(
            "activities_list_image", "class",
            url=self.live_server_url + '/act/public/'
        )
