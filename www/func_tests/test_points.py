from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase
from activities.models import Act
from post.models import Post


class PointWebdriver(BaseTestStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.email = 'just_test@test.com'
        cls.password = '123456saasdfasdf'
        cls.username = 'just_test'
        super(PointWebdriver, cls).setUpClass()

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

    def test_like_other_posts_minus_point(self):
        self.email2 = 'just_test_other@test.com'
        self.password2 = '123456saasdsdfsdfasdf'
        self.username2 = 'just_test_other'
        self.user_object2 = get_user_model().objects.create_user(
                username=self.username2,
                email=self.email2,
                password=self.password2,
                is_active=1
            )
        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '1490031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        self.act_type = 2
        self.act_object = Act.objects.create(
            user=self.user_object2,
            act_title=self.act_title,
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=self.act_type,
            act_ident=10,
            act_url=self.username2 + '/' + self.act_title,
            )
        self.post_content = 'just_sample_content'
        self.post_thumb_url = '1457502382959cf00'
        self.post_thumb_width = 500.0
        self.post_thumb_height = 1000.0
        self.post_mime_types = 1
        self.nsfw = 1
        self.post_object = Post.objects.create(
            act=self.act_object,
            user=self.user_object2,
            post_content=self.post_content,
            post_thumb_url=self.post_thumb_url,
            post_thumb_width=self.post_thumb_width,
            post_thumb_height=self.post_thumb_height,
            post_mime_types=self.post_mime_types,
            nsfw=self.nsfw,
        )
        self.driver.get(
            self.live_server_url + '/act/' +
            self.username2 + '/' + self.act_title + '/'
        )
        self.driver.find_element_by_class_name(
            'post-thumb-a').click()
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "post-like-details-a"))
            )
        finally:
            self.driver.find_element_by_class_name(
                'post-like-details').click()
        self.assertEqual(49, self.user_object.points)
