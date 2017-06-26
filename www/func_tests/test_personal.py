from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase
from activities.models import Act
from post.models import Post


class PersonalWebdriver(BaseTestStaticLiveServerTestCase):

    def setUp(self):
        self.username = 'just_test'
        self.email = 'just_test@test.com'
        self.password = '123456saasdfasdf'
        self.live_server_url = 'http://web:8081'
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
    def test_personal_act_create_empty_default(self):
        self.driver.get(
            self.live_server_url + '/' + self.username + '/act_create/')
        self.assert_equal_error_text(
            'feed-empty',
            'You haven\'t create any activities yet.')

    def test_personal_act_join_empty_default(self):
        self.driver.get(
            self.live_server_url + '/' + self.username + '/act_join/')
        self.assert_equal_error_text(
            'feed-empty',
            'You haven\'t join any activities yet.')

    def test_personal_act_post_empty_default(self):
        self.driver.get(
            self.live_server_url + '/' + self.username + '/post/')
        self.assert_equal_error_text(
            'feed-empty',
            'You haven\'t join any activities yet.')

    def test_personal_act_create_success(self):
        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '147326964570df47ebce96cc7' + \
                             'bd661f788786d51c16afce068'
        self.act_type = 2
        self.act = Act.objects.create(
            user=self.user_object,
            act_title=self.act_title,
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=self.act_type,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.driver.get(
            self.live_server_url + '/' + self.username + '/act_create/')
        feed_empty = self.driver.find_elements_by_class_name('feed-empty')
        self.assertFalse(bool(feed_empty))
        act_title = self.driver.find_element_by_class_name(
            'act-title-p')
        self.assertEqual(act_title.text, 'just a test title')

    def test_personal_act_join_success(self):
        self.email2 = '2just_test@test.com'
        self.password2 = '2123456saasdfasdf'
        self.username2 = '2just_test'
        self.user_object2 = get_user_model().objects.create_user(
                username=self.username2,
                email=self.email2,
                password=self.password2,
                is_active=1
        )
        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '147326964570df47ebce96cc7' + \
                             'bd661f788786d51c16afce068'
        self.act_type = 2
        self.post_content = 'just_sample_content'
        self.post_thumb_url = '1457502382959cf00'
        self.post_thumb_width = 500.0
        self.post_thumb_height = 1000.0
        self.post_mime_types = 1
        self.nsfw = 1
        self.act_object = Act.objects.create(
            user=self.user_object2,
            act_title=self.act_title,
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=self.act_type,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.post_object = Post.objects.create(
            act=self.act_object,
            user=self.user_object,
            post_content=self.post_content,
            post_thumb_url=self.post_thumb_url,
            post_thumb_width=self.post_thumb_width,
            post_thumb_height=self.post_thumb_height,
            post_mime_types=self.post_mime_types,
            nsfw=self.nsfw,
        )
        self.driver.get(
            self.live_server_url + '/' + self.username + '/act_join/')
        feed_empty = self.driver.find_elements_by_class_name('feed-empty')
        self.assertFalse(bool(feed_empty))
        act_title = self.driver.find_element_by_class_name(
            'act-title-p')
        self.assertEqual(act_title.text, 'just a test title')
