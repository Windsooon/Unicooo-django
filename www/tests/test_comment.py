from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from post.models import Post
from comment.models import Comment
from activities.models import Act


class PostTestCase(TestCase):
    def setUp(self):
        self.server = 'http://127.0.0.1'
        self.email = 'just_test@test.com'
        self.password = '123456saasdfasdf'
        self.username = 'just_test'
        active = {'is_active': 1}
        self.user_object = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                options=active,
            )
        # second user
        self.email2 = '2just_test@test.com'
        self.password2 = '2123456saasdfasdf'
        self.username2 = '2just_test'
        self.user_object2 = get_user_model().objects.create_user(
                username=self.username2,
                email=self.email2,
                password=self.password2,
                options=active,
            )
        self.client = Client()
        self.client.force_login(self.user_object)

        # act default vale
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

        # comment default value
        self.comment_content = 'just a test 你 comment'
        self.comment_object = Comment.objects.create(
            post=self.post_object,
            user=self.user_object,
            reply_id=1,
            comment_content=self.comment_content
        )

    def test_create_new_same_comment(self):
        response = self.client.post('/api/comments/', {
            'post': self.post_object.id,
            'user': self.user_object.id,
            'reply_id': 1,
            'comment_content': self.comment_content
        })
        self.assertEqual(response.status_code, 201)

    def test_create_new_comment_logout_failed(self):
        self.client.logout()
        response = self.client.post('/api/comments/', {
            'post': self.post_object.id,
            'user': self.user_object.id,
            'reply_id': 1,
            'comment_content': self.comment_content
        })
        self.assertEqual(response.status_code, 403)

    def test_modify_comment_failed(self):
        modify_comment = 'jusut modify你就comment'
        response = self.client.post(
            '/api/comments/' +
            str(self.comment_object.id) + '/', {
                'post': self.post_object.id,
                'user': self.user_object.id,
                'reply_id': 1,
                'comment_content': modify_comment
            })
        self.assertEqual(response.status_code, 405)

    def test_delete_comment_failed(self):
        response = self.client.delete(
            '/api/comments/' +
            str(self.comment_object.id) + '/', {
            })
        self.assertEqual(response.status_code, 405)
