import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase
from activities.models import Act
from post.models import Post


class PostWebdriver(BaseTestStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):

        super(PostWebdriver, cls).setUpClass()

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

    def test_create_post(self):
        self.driver.get(self.live_server_url)
        self.driver.get(
            self.live_server_url + '/act/' +
            self.username + '/' + self.act_title + '/')
        self.driver.find_element_by_class_name(
            'join-act-btn').send_keys(Keys.ENTER)
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "post-form-text"))
            )
        finally:
            self.driver.find_element_by_class_name(
                'post-upload-image').send_keys(
                '/usr/src/app/func_tests/images/images_test.png')
            time.sleep(6)
            self.driver.find_element_by_class_name('post-form-text').send_keys(
                'just_for_test_content')
            self.driver.find_element_by_class_name('add-post-btn').send_keys(
                Keys.ENTER)
            time.sleep(3)
            self.assertEqual(Post.objects.count(), 1)

    def test_create_post_with_valid_url(self):
        self.driver.find_element_by_class_name(
            'join-act-btn').send_keys(Keys.ENTER)
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "post-form-text"))
            )
        finally:
            self.driver.find_element_by_class_name(
                'post-upload-image').send_keys(
                '/usr/src/app/func_tests/images/images_test.png')
            time.sleep(6)
            self.driver.find_element_by_class_name('post-form-text').send_keys(
                'just_for_test_content')
            add_url_btn = self.driver.find_element_by_class_name('add-url-btn')
            add_url_btn.click()
            try:
                WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "post-form-url"))
                )
            finally:
                self.driver.find_element_by_class_name(
                    'post-form-url').send_keys('www.bing.com')
                self.driver.find_element_by_class_name(
                    'add-post-btn').send_keys(Keys.ENTER)
                time.sleep(3)
                self.assertEqual(Post.objects.count(), 1)

    def test_create_post_with_http_valid_url(self):
        self.driver.find_element_by_class_name(
            'join-act-btn').send_keys(Keys.ENTER)
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "post-form-text"))
            )
        finally:
            self.driver.find_element_by_class_name(
                'post-upload-image').send_keys(
                '/usr/src/app/func_tests/images/images_test.png')
            time.sleep(5)
            self.driver.find_element_by_class_name('post-form-text').send_keys(
                'just_for_test_content')
            add_url_btn = self.driver.find_element_by_class_name('add-url-btn')
            add_url_btn.click()
            try:
                WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "post-form-url"))
                )
            finally:
                self.driver.find_element_by_class_name(
                    'post-form-url').send_keys('http://www.bing.com')
                self.driver.find_element_by_class_name(
                    'add-post-btn').send_keys(Keys.ENTER)
                time.sleep(3)
                self.assertEqual(Post.objects.count(), 1)

    def test_create_post_with_https_valid_url(self):
        self.driver.find_element_by_class_name(
            'join-act-btn').send_keys(Keys.ENTER)
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "post-form-text"))
            )
        finally:
            self.driver.find_element_by_class_name(
                'post-upload-image').send_keys(
                '/usr/src/app/func_tests/images/images_test.png')
            time.sleep(5)
            self.driver.find_element_by_class_name('post-form-text').send_keys(
                'just_for_test_content')
            add_url_btn = self.driver.find_element_by_class_name('add-url-btn')
            add_url_btn.click()
            try:
                WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "post-form-url"))
                )
            finally:
                self.driver.find_element_by_class_name(
                    'post-form-url').send_keys('https://www.bing.com')
                self.driver.find_element_by_class_name(
                    'add-post-btn').send_keys(Keys.ENTER)
                time.sleep(3)
                self.assertEqual(Post.objects.count(), 1)

    def test_create_post_with_not_valid_url_failed(self):
        self.driver.find_element_by_class_name(
            'join-act-btn').send_keys(Keys.ENTER)
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "post-form-text"))
            )
        finally:
            self.driver.find_element_by_class_name(
                'post-upload-image').send_keys(
                '/usr/src/app/func_tests/images/images_test.png')
            time.sleep(6)
            self.driver.find_element_by_class_name('post-form-text').send_keys(
                'just_for_test_content')
            self.driver.find_element_by_class_name('add-url-btn').click()
            self.driver.find_element_by_class_name('add-url-btn').send_keys(
                'sadfasdfasdfasdf')
            self.driver.find_element_by_class_name('add-post-btn').send_keys(
                Keys.ENTER)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.alert_is_present(), 'timeout'
                )
            finally:
                alert = self.driver.switch_to_alert()
                self.assertEqual(alert.text, 'Url not valid.')
