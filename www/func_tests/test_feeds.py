from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase
from activities.models import Act
from post.models import Post


class FeedWebdriver(BaseTestStaticLiveServerTestCase):

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

        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '1490031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        self.act_type = 1
        self.act_object = Act.objects.create(
            user=self.user_object,
            act_title=self.act_title,
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=self.act_type,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )

    def tearDown(self):
        pass

    def test_feed_empty_by_default(self):
        self.driver.get(self.live_server_url + '/' + self.username + '/feed/')
        self.assert_equal_error_text(
            'feed-empty',
            'You haven\'t join any activities yet.')

    def test_feed_get_post_when_create_act_then_join(self):
        # post default vale
        self.post_content = 'just_sample_content'
        self.post_thumb_url = '1457502382959cf00'
        self.post_thumb_width = 500.0
        self.post_thumb_height = 1000.0
        self.post_mime_types = 1
        self.nsfw = 1
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

        self.driver.get(self.live_server_url + '/' + self.username + '/feed/')
        feed_empty = self.driver.find_elements_by_class_name('feed-empty')
        self.assertFalse(bool(feed_empty))
        post_text = self.driver.find_element_by_class_name('post-content-p')
        self.assertEqual('just_sample_content', post_text.text)

    def test_feed_get_post_when_other_create_act_then_join(self):
        # post default vale
        self.user_object2 = get_user_model().objects.create_user(
            username='test_user_name',
            email='test@testuser.com',
            password=self.password,
            is_active=1
            )
        self.post_content = 'just_sample_content'
        self.post_thumb_url = '1457502382959cf00'
        self.post_thumb_width = 500.0
        self.post_thumb_height = 1000.0
        self.post_mime_types = 1
        self.nsfw = 1
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

        self.driver.get(self.live_server_url + '/' + self.username + '/feed/')
        feed_empty = self.driver.find_elements_by_class_name('feed-empty')
        self.assertFalse(bool(feed_empty))
        post_text = self.driver.find_element_by_class_name('post-content-p')
        self.assertEqual('just_sample_content', post_text.text)
