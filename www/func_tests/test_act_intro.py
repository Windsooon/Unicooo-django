from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase
from activities.models import Act


class IntroWebdriver(BaseTestStaticLiveServerTestCase):

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
        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '1490031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        self.act_type = 1
        self.act = Act.objects.create(
            user=self.user_object,
            act_title=self.act_title,
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=self.act_type,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.client = Client()
        self.client.force_login(self.user_object)
        self.cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/act/new/')
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': self.cookie.value,
            'secure': False, 'path': '/'})
        self.driver.get(
            self.live_server_url + '/act/' +
            self.username + '/' + self.act_title + '/')

    def tearDown(self):
        self.client.logout()

    def test_act_intro_default_empty(self):
        self.driver.find_element_by_class_name(
            'details-act-btn').send_keys(Keys.ENTER)
        self.wait_element_url(
            'act-editor', url=self.live_server_url + '/' +
            'act/just_test/just%20a%20test%20title/details/'
        )
        editor = self.driver.find_element_by_class_name('ql-editor')
        edit_btn = self.driver.find_element_by_id('act-edit-btn')
        self.assertEqual(editor.text, 'Nothing yet.')
        self.assertEqual(edit_btn.text, 'EDIT')

    def test_add_act_intro(self):
        self.driver.get(
            self.live_server_url + '/' +
            'act/just_test/just%20a%20test%20title/details/')
        editor = self.driver.find_element_by_class_name('ql-editor')
        edit_btn = self.driver.find_element_by_id('act-edit-btn')
        edit_btn.click()
        self.assertEqual(edit_btn.text, 'SAVE')
        editor.clear()
        fake_text = (
            'Lorem Ipsum is simply dummy text of the printing' +
            '你好这是测试'
        )
        editor.send_keys(fake_text)
        edit_btn.click()
        self.assertEqual(edit_btn.text, 'EDIT')
        self.driver.refresh()
        editor = self.driver.find_element_by_class_name('ql-editor')
        self.assertEqual(editor.text, fake_text + ' ')
