from django.contrib.auth import get_user_model
from django.test import Client
from .base_tests import BaseTestStaticLiveServerTestCase
from activities.models import Act
from post.models import Post
from comment.models import Comment


class FeedWebdriver(BaseTestStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.email = 'just_test@test.com'
        cls.password = '123456saasdfasdf'
        cls.username = 'just_test'
        super(FeedWebdriver, cls).setUpClass()

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

    def test_comment_empty_by_default(self):
        self.driver.get(
            self.live_server_url + '/' +
            self.username + '/comments/')
        self.assert_equal_error_text(
            'empty-comment-p',
            'Nothing yet.', 'class')

    def test_get_comments_when_other_comment(self):
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
        self.user_object2 = get_user_model().objects.create_user(
                username='just_test_comment',
                email='just_test_comment@test.com',
                password='1231242343243',
                is_active=1
        )
        self.comment_object = Comment.objects.create(
            post=self.post_object,
            user=self.user_object2,
            reply_id=self.user_object.id,
            comment_content='just_test_comment'
        )
        self.driver.get(
            self.live_server_url + '/' +
            self.username + '/comments/')
        empty_comment = self.driver.find_elements_by_class_name(
            'empty-comment-p')
        self.assertFalse(bool(empty_comment))
        comment = self.driver.find_element_by_class_name(
            'comment-content-p')
        self.assertEqual(comment.text, 'just_test_comment')
