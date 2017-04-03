import json
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from activities.models import Act


class ActTestCase(TestCase):
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
        self.user_object = get_user_model(). \
            objects.get(id=self.user.id)
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
            objects.get(id=self.user2.id)

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
        self.act_object = Act.objects.get(id=self.act.id)

    def test_create_new_act_without_login(self):
        self.client.logout()
        act_title = 'just a test st'
        act_content = 'just a test content, content'
        act_thumb_url = '1490031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        # 0 for personal, 1 for group, 2 for public
        act_type = 1
        response = self.client.post('/api/acts/', {
            'act_title': act_title,
            'act_content': act_content,
            'act_thumb_url': act_thumb_url,
            'act_type': act_type,
            'act_ident': 20,
            'act_url': self.username + act_title,
        })
        self.assertEqual(response.status_code, 403)

    def test_modify_act_without_login(self):
        self.client.logout()
        act_c_title = 'just a change title'
        act_c_content = 'just a change content, content'
        act_c_thumb_url = '888888814968b2eaff2f9ae1a02ec01108757eb768d81dfc'
        json_data = {
            'act_title': act_c_title,
            'act_content': act_c_content,
            'act_thumb_url': act_c_thumb_url,
            'act_url': self.username + '/' + act_c_title,
        }
        response = self.client.put(
            '/api/acts/' + str(self.act_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_delete_act_without_login(self):
        self.client.logout()
        response = self.client.delete(
            '/api/acts/' + str(self.act_object.id) + '/')
        self.assertEqual(response.status_code, 403)

    def test_create_new_act(self):
        act_title = 'just a test st'
        act_content = 'just a tests content, content'
        act_thumb_url = '149d0031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        # 0 for personal, 1 for group, 2 for public
        act_type = 1
        response = self.client.post('/api/acts/', {
            'act_title': act_title,
            'act_content': act_content,
            'act_thumb_url': act_thumb_url,
            'act_type': act_type,
            'act_ident': 20,
            'act_url': self.username + act_title,
        })
        self.assertEqual(response.status_code, 201)
        act = Act.objects.get(act_title=act_title)
        self.assertEqual(act.act_title, act_title)
        self.assertEqual(act.act_title, act_title)
        self.assertEqual(act.act_content, act_content)
        self.assertEqual(act.act_star, 0)
        self.assertEqual(act.act_status, 0)
        self.assertEqual(act.user_id, self.user.id)
        self.assertEqual(act.act_thumb_url, act_thumb_url)
        self.assertEqual(act.act_url, self.username + act_title)

    def test_create_new_act_sametitle_failed(self):
        act_title = 'just a test title'
        act_content = 'just a tests content, content'
        act_thumb_url = '149d0031868b2eaff2f9ae1a02ec01108757eb768d81dfc'
        # 0 for personal, 1 for group, 2 for public
        act_type = 1

        with self.assertRaisesMessage(
            django.db.utils.IntegrityError,
            'UNIQUE constraint failed: activities_act.user_id, ' +
                'activities_act.act_title'):
            self.client.post('/api/acts/', {
                'act_title': act_title,
                'act_content': act_content,
                'act_thumb_url': act_thumb_url,
                'act_type': act_type,
                'act_ident': 20,
                'act_url': self.username + act_title,
            })

    def test_modify_act(self):
        act_c_title = 'just a change title'
        act_c_content = 'just a change content, content'
        act_c_thumb_url = '888888814968b2eaff2f9ae1a02ec01108757eb768d81dfc'
        json_data = {
            'act_title': act_c_title,
            'act_content': act_c_content,
            'act_thumb_url': act_c_thumb_url,
            'act_url': self.username + '/' + act_c_title,
        }
        response = self.client.put(
            '/api/acts/' + str(self.act_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        act = Act.objects.get(act_title=act_c_title)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(act.act_title, act_c_title)
        self.assertEqual(act.act_content, act_c_content)
        self.assertEqual(act.act_star, 0)
        self.assertEqual(act.act_status, 0)
        self.assertEqual(act.user_id, self.user.id)
        self.assertEqual(act.act_thumb_url, act_c_thumb_url)
        self.assertEqual(act.act_url, self.username + '/' + act_c_title)

    def test_modify_act_from_otheruser_failed(self):
        self.client.logout()
        self.client.force_login(self.user2)
        act_c_title = 'just a change title'
        act_c_content = 'just a change content, content'
        act_c_thumb_url = '888888814968b2eaff2f9ae1a02ec01108757eb768d81dfc'
        json_data = {
            'act_title': act_c_title,
            'act_content': act_c_content,
            'act_thumb_url': act_c_thumb_url,
            'act_url': self.username + '/' + act_c_title,
        }
        response = self.client.put(
            '/api/acts/' + str(self.act_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_delete_act(self):
        response = self.client.delete(
            '/api/acts/' + str(self.act_object.id) + '/')
        self.assertEqual(response.status_code, 204)
        act = Act.objects.filter(act_title=self.act_title)
        self.assertFalse(act.exists())

    def test_delete_act_from_otheruser_failed(self):
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.delete(
            '/api/acts/' + str(self.act_object.id) + '/')
        self.assertEqual(response.status_code, 403)

    def test_act_title_too_long(self):
        act_c_title = 'just a change title,aui你会sdfaksdfjasdfj'
        act_c_content = 'just a change content, content'
        act_c_thumb_url = '888888814968b2eaff2f9ae1a02ec01108757eb768d81dfc'
        json_data = {
            'act_title': act_c_title,
            'act_content': act_c_content,
            'act_thumb_url': act_c_thumb_url,
            'act_url': self.username + '/' + act_c_title,
        }
        response = self.client.put(
            '/api/acts/' + str(self.act_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_act_content_too_long(self):
        act_c_title = 'just a change title'
        act_c_content = 'just a change content, content'*100
        act_c_thumb_url = '888888814968b2eaff2f9ae1a02ec01108757eb768d81dfc'
        json_data = {
            'act_title': act_c_title,
            'act_content': act_c_content,
            'act_thumb_url': act_c_thumb_url,
            'act_url': self.username + '/' + act_c_title,
        }
        response = self.client.put(
            '/api/acts/' + str(self.act_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_new_act_without_title(self):
        act_c_content = 'just a change content, content'
        act_c_thumb_url = '888888814968b2eaff2f9ae1a02ec01108757eb768d81dfc'
        json_data = {
            'act_content': act_c_content,
            'act_thumb_url': act_c_thumb_url,
            'act_url': self.username + '/',
        }
        response = self.client.put(
            '/api/acts/' + str(self.act_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
