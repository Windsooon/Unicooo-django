from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from post.models import Post
from activities.models import Act


class PostTestCase(TestCase):
    def setUp(self):
        self.server = 'http://127.0.0.1'
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
        # second user
        self.email2 = '2just_test@test.com'
        self.password2 = '2123456saasdfasdf'
        self.username2 = '2just_test'
        self.user2 = get_user_model().objects.create_user(
                username=self.username2,
                email=self.email2,
                password=self.password2,
                options=active,
            )
        self.user_object2 = get_user_model(). \
            objects.get(email='2just_test@test.com')

        self.client = Client()
        self.client.force_login(self.user)
        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '1490031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        self.act_type = 1
        self.client.post('/api/acts/', {
            'act_title': self.act_title,
            'act_content': self.act_content,
            'act_thumb_url': self.act_thumb_url,
            'act_type': self.act_type,
            'act_ident': 20,
            'act_url': self.username + '/' + self.act_title,
        })
        self.act_object = Act.objects.get(act_title=self.act_title)
