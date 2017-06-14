import json
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
        self.user_object = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                is_active=1,
            )
        # second user
        self.email2 = '2just_test@test.com'
        self.password2 = '2123456saasdfasdf'
        self.username2 = '2just_test'
        self.user_object2 = get_user_model().objects.create_user(
                username=self.username2,
                email=self.email2,
                password=self.password2,
                is_active=1
            )
        self.client = Client()
        self.client.force_login(self.user_object)

        # act default value
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

    def test_create_new_same_post(self):
        response = self.client.post('/api/posts/', {
            'act': self.act_object.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 201)

    def test_create_new_post_content_too_long(self):
        post_long_content = "asdflasdfsafsadfjaskdfjasf" + \
                            "askdjfsldjfaskdfjsadfjsdfj" + \
                            "askdjfsldjfaskdfjsadfjsdfj" + \
                            "askdjfsldjfaskdfjsadfjsdfj" + \
                            "askdjfsldjfaskdfjsadfjsdfj" + \
                            "askdjfsldjfaskdfjsadfjsdfj"
        response = self.client.post('/api/posts/', {
            'act': self.act_object.id,
            'post_content': post_long_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 400)

    def test_modify_post(self):
        post_c_content = 'modify_post_content'
        post_c_thumb_url = 'modify_url'
        post_c_thumb_width = 100.0
        post_c_thumb_height = 200.0
        json_data = {
            'act': self.act_object.id,
            'user': self.user_object.id,
            'post_content': post_c_content,
            'post_thumb_url': post_c_thumb_url,
            'post_thumb_width': post_c_thumb_width,
            'post_thumb_height': post_c_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        }
        response = self.client.put(
            '/api/posts/' + str(self.post_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        post_object = Post.objects.get(id=self.post_object.id)
        self.assertEqual(post_object.post_content, post_c_content)
        self.assertEqual(post_object.post_thumb_url, post_c_thumb_url)
        self.assertEqual(post_object.post_thumb_width, post_c_thumb_width)
        self.assertEqual(post_object.post_thumb_height, post_c_thumb_height)

    def test_delete_post(self):
        response = self.client.delete(
            '/api/posts/' + str(self.post_object.id) + '/',
            content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_modify_post_without_content(self):
        post_c_thumb_url = 'modify_url'
        post_c_thumb_width = 100.0
        post_c_thumb_height = 200.0
        json_data = {
            'act': self.act_object.id,
            'user': self.user_object.id,
            'post_thumb_url': post_c_thumb_url,
            'post_thumb_width': post_c_thumb_width,
            'post_thumb_height': post_c_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        }
        response = self.client.patch(
            '/api/posts/' + str(self.post_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        post_object = Post.objects.get(id=self.post_object.id)
        self.assertEqual(post_object.post_content, self.post_content)
        self.assertEqual(post_object.post_thumb_url, post_c_thumb_url)
        self.assertEqual(post_object.post_thumb_width, post_c_thumb_width)
        self.assertEqual(post_object.post_thumb_height, post_c_thumb_height)

    def test_modify_post_without_url(self):
        post_c_content = 'modify_post_content'
        post_c_thumb_width = 100.0
        post_c_thumb_height = 200.0
        json_data = {
            'act': self.act_object.id,
            'user': self.user_object.id,
            'post_content': post_c_content,
            'post_thumb_width': post_c_thumb_width,
            'post_thumb_height': post_c_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        }
        response = self.client.patch(
            '/api/posts/' + str(self.post_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        post_object = Post.objects.get(id=self.post_object.id)
        self.assertEqual(post_object.post_content, post_c_content)
        self.assertEqual(post_object.post_thumb_url, self.post_thumb_url)
        self.assertEqual(post_object.post_thumb_width, post_c_thumb_width)
        self.assertEqual(post_object.post_thumb_height, post_c_thumb_height)

    def test_modify_ohter_user_post_failed(self):
        self.client.logout()
        self.client.force_login(self.user_object2)
        post_c_content = 'modify_post_content'
        post_c_thumb_url = 'modify_url'
        post_c_thumb_width = 100.0
        post_c_thumb_height = 200.0
        json_data = {
            'act': self.act_object.id,
            'user': self.user_object.id,
            'post_content': post_c_content,
            'post_thumb_url': post_c_thumb_url,
            'post_thumb_width': post_c_thumb_width,
            'post_thumb_height': post_c_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        }
        response = self.client.put(
            '/api/posts/' + str(self.post_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_modify_post_logout_failed(self):
        self.client.logout()
        post_c_content = 'modify_post_content'
        post_c_thumb_url = 'modify_url'
        post_c_thumb_width = 100.0
        post_c_thumb_height = 200.0
        json_data = {
            'act': self.act_object.id,
            'user': self.user_object.id,
            'post_content': post_c_content,
            'post_thumb_url': post_c_thumb_url,
            'post_thumb_width': post_c_thumb_width,
            'post_thumb_height': post_c_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        }
        response = self.client.put(
            '/api/posts/' + str(self.post_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_create_new_same_post_logout_failed(self):
        self.client.logout()
        response = self.client.post('/api/posts/', {
            'act': self.act_object.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_post_logout(self):
        self.client.logout()
        response = self.client.delete(
            '/api/posts/' + str(self.post_object.id) + '/',
            content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_other_delete_post_failed(self):
        self.client.logout()
        self.client.force_login(self.user_object2)
        response = self.client.delete(
            '/api/posts/' + str(self.post_object.id) + '/',
            content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_admin_delete_post(self):
        self.admin_user = get_user_model().objects.create_user(
            username='admin_user',
            email='admin@admin.com',
            password=self.password,
            is_active=1,
            is_admin=1
            )
        self.client.logout()
        self.client.force_login(self.admin_user)

        response = self.client.delete(
            '/api/posts/' + str(self.post_object.id) + '/',
            content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_public_acts_author_can_join(self):
        public_act = Act.objects.create(
            user=self.user_object,
            act_title='public_act',
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=2,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.client = Client()
        self.client.force_login(self.user_object)
        response = self.client.post('/api/posts/', {
            'act': public_act.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 201)

    def test_public_acts_other_can_join(self):
        public_act = Act.objects.create(
            user=self.user_object,
            act_title='public_act',
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=2,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.client = Client()
        self.client.force_login(self.user_object2)
        response = self.client.post('/api/posts/', {
            'act': public_act.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 201)

    def test_group_acts_author_can_join(self):
        group_act = Act.objects.create(
            user=self.user_object,
            act_title='public_act',
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=1,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.client = Client()
        self.client.force_login(self.user_object)
        response = self.client.post('/api/posts/', {
            'act': group_act.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 201)

    def test_group_acts_other_can_join(self):
        group_act = Act.objects.create(
            user=self.user_object,
            act_title='public_act',
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=1,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.client = Client()
        self.client.force_login(self.user_object2)
        response = self.client.post('/api/posts/', {
            'act': group_act.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 201)

    def test_private_acts_author_can_join(self):
        private_act = Act.objects.create(
            user=self.user_object,
            act_title='public_act',
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=0,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.client = Client()
        self.client.force_login(self.user_object)
        response = self.client.post('/api/posts/', {
            'act': private_act.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 201)

    def test_private_acts_other_join_failed(self):
        private_act = Act.objects.create(
            user=self.user_object,
            act_title='public_act',
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=0,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.client = Client()
        self.client.force_login(self.user_object2)
        response = self.client.post('/api/posts/', {
            'act': private_act.id,
            'post_content': self.post_content,
            'post_thumb_url': self.post_thumb_url,
            'post_thumb_width': self.post_thumb_width,
            'post_thumb_height': self.post_thumb_height,
            'post_mime_types': self.post_mime_types,
            'nsfw': self.nsfw,
        })
        self.assertEqual(response.status_code, 403)
