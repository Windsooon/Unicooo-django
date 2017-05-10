import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.cache import cache
from django.core.urlresolvers import reverse
from rest_framework.compat import is_anonymous


class visitPageTest(TestCase):

    def setUp(self):
        self.server = 'http://127.0.0.1'
        # first user
        self.email = 'just_test@test.com'
        self.password = '123456saasdfasdf'
        self.username = 'just_test'
        self.login_required_url = '/act/new/'
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
        self.client.force_login(self.user_object)

    def test_user_info(self):
        self.assertEqual('just_test@test.com', self.user_object.email)
        self.assertEqual('just_test', self.user_object.user_name)

    def redirect_to_home(
            self, response,
            expected_url='/login/?next=/act/new/',
            status_code=302,
            target_status_code=200):

        self.assertRedirects(
            response,
            expected_url=expected_url,
            status_code=status_code,
            target_status_code=target_status_code)

    def test_create_user(self):
        self.client.logout()
        response = self.client.post('/api/users/', {
            'user_name': 'just_create_user',
            'email': 'just_create_user@gmail.com',
            'password': 'just_create_password',
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_without_email(self):
        self.client.logout()
        response = self.client.post('/api/users/', {
            'user_name': 'just_create_user',
            'password': 'just_create_password',
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_without_username(self):
        self.client.logout()
        response = self.client.post('/api/users/', {
            'email': 'just_create_user@gmail.com',
            'password': 'just_create_password',
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_without_password(self):
        self.client.logout()
        response = self.client.post('/api/users/', {
            'user_name': 'just_create_user',
            'email': 'just_create_user@gmail.com',
        })
        self.assertEqual(response.status_code, 400)

    def test_modify_user_name(self):
        json_data = {
            'user_name': 'just_modify_user',
        }
        response = self.client.patch(
            '/api/users/' + str(self.user_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_modify_user_email(self):
        json_data = {
            'email': 'just_modify_user@test.com',
        }
        response = self.client.patch(
            '/api/users/' + str(self.user_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            get_user_model().objects.filter
            (email='just_modify_user@test.com').exists())

    def test_modify_user_email_illegal(self):
        json_data = {
            'email': 'just_modify_usertest.com',
        }
        response = self.client.patch(
            '/api/users/' + str(self.user_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_modify_user_without_user_name(self):
        json_data = {
            'email': 'just_modify_user@gmail.com',
            'user_details': 'just_modify_details',
            'user_avatar': '12121231313311',
        }
        response = self.client.patch(
            '/api/users/' + str(self.user_object.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_modify_other_user_failed(self):
        json_data = {
            'user_name': 'just_modify_user',
            'email': 'just_modify_user@gmail.com',
            'user_details': 'just_modify_details',
        }
        response = self.client.put(
            '/api/users/' + str(self.user_object2.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_modify_other_user_patch_failed(self):
        json_data = {
            'email': 'just_modify_user@gmail.com',
            'user_details': 'just_modify_details',
        }
        response = self.client.patch(
            '/api/users/' + str(self.user_object2.id) + '/',
            json.dumps(json_data), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_login(self):
        self.client.logout()
        self.client.login(
            email=self.email, password=self.password)
        response = self.client.get(self.login_required_url)
        self.assertEqual(response.status_code, 200)

    def test_wrong_email(self):
        self.client.logout()
        self.client.login(
            email='wrongemail@email.com', password=self.password)
        response = self.client.get(self.login_required_url)
        self.redirect_to_home(response)

    def test_wrong_password(self):
        self.client.logout()
        self.client.login(
            email=self.email, password='just_wrong_password')
        response = self.client.get(self.login_required_url)
        self.redirect_to_home(response)

    def test_login_without_email(self):
        self.client.logout()
        self.client.login(
            password=self.password)
        response = self.client.get(self.login_required_url)
        self.redirect_to_home(response)

    def test_login_withour_password(self):
        self.client.logout()
        self.client.login(
            password=self.password)
        response = self.client.get(self.login_required_url)
        self.redirect_to_home(response)

    def test_logout(self):
        self.assertFalse(is_anonymous(self.user_object))
        self.client.logout()
        response = self.client.get(self.login_required_url)
        self.redirect_to_home(response)

    def test_get_comments(self):
        response = self.client.get('/' + self.username + '/comments/')
        self.assertEqual(response.status_code, 200)

    def test_get_settings(self):
        self.client.force_login(self.user_object)
        response = self.client.get('/' + self.username + '/settings/')
        self.assertEqual(response.status_code, 200)

    def test_all_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/act/public/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/token/')
        self.assertEqual(response.status_code, 400)

    def test_login_signup(self):
        response = self.client.get('/signup/')
        self.assertRedirects(
            response,
            expected_url='/',
            status_code=302,
            target_status_code=200)

    def test_login_login(self):
        response = self.client.get('/login/?next=/')
        self.assertRedirects(
            response,
            expected_url=reverse('front_page'),
            status_code=302,
            target_status_code=200)

    def test_check_email(self):
        response = self.client.get('/checkemail/')
        self.assertEqual(response.status_code, 200)

    def test_check_user(self):
        response = self.client.get('/checkuser/')
        self.assertEqual(response.status_code, 200)

    def test_check_act_title(self):
        response = self.client.get('/act_title/')
        self.assertEqual(response.status_code, 200)

    def test_user_points(self):
        self.assertEqual(
            cache.get("user_points_" + str(self.user_object.id)), 50)
