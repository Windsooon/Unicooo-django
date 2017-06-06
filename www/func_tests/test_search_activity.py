import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from activities.models import Act


class VisitFronePageWebdriver(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(VisitFronePageWebdriver, cls).setUpClass()
        cls.display = Display(visible=0, size=(1024, 800))
        cls.display.start()
        cls.driver = webdriver.Firefox(
            executable_path='/usr/src/app/selenium_sources/geckodriver')
        cls.driver.set_window_size(1024, 768)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.display.stop()
        super(VisitFronePageWebdriver, cls).tearDownClass()

    def tearDown(self):
        pass

    def test_search_empty(self):
        '''
        search return nothing
        '''
        self.driver.get(self.live_server_url + '/')
        self.driver.find_element_by_class_name('act-search').click()
        alert = self.driver.switch_to_alert()
        self.assertEqual(alert.text, 'Please enter activity id for searching.')

    def test_search_no_activity(self):
        '''
        search return nothing
        '''
        self.driver.get(self.live_server_url + '/')
        self.driver.find_element_by_class_name(
            'act-search-text').send_keys(10080)
        self.driver.find_element_by_class_name(
            'act-search-text').send_keys(Keys.ENTER)
        alert = self.driver.switch_to_alert()
        self.assertEqual(alert.text, 'Can\'t find this activity')

    def test_search_correct(self):
        '''
        search return nothing
        '''
        self.email = 'just_test@test.com'
        self.password = '123456saasdfasdf'
        self.username = 'just_test'
        active = {'is_active': 1}
        self.user = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                options=active,
            )
        self.user_object = get_user_model(). \
            objects.get(id=self.user.id)
        self.client = Client()
        self.client.force_login(self.user)
        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '1490031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        self.act_type = 1
        self.act = Act.objects.create(
            user=self.user,
            act_title=self.act_title,
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=self.act_type,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.driver.get(self.live_server_url + '/')
        act_search = self.driver.find_element_by_class_name('act-search-text')
        act_search.send_keys('10001')
        self.driver.find_element_by_class_name(
            'act-search-text').send_keys(Keys.ENTER)
