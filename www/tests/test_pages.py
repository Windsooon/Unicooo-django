from django.test import TestCase
from django.core.urlresolvers import reverse


class visitPageTest(TestCase):
    def test_frontpage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login/')
        self.assertRedirects(
            response,
            expected_url=reverse('login') + '?next=/',
            status_code=302,
            target_status_code=200)

    def test_check_email(self):
        response = self.client.get('/checkemail/')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_public_acts(self):
        response = self.client.get('/act/public/')
        self.assertEqual(response.status_code, 200)

    def test_get_token(self):
        response = self.client.get('/token/')
        self.assertRedirects(
            response,
            expected_url=reverse('login') + '?next=/token/',
            status_code=302,
            target_status_code=200)

    def test_check_user(self):
        response = self.client.get('/checkuser/')
        self.assertEqual(response.status_code, 200)

    def test_check_act_title(self):
        response = self.client.get('/act_title/')
        self.assertEqual(response.status_code, 200)

    def test_check_act_new(self):
        response = self.client.get('/act/new/')
        self.assertRedirects(
            response,
            expected_url=reverse('login') + '?next=/act/new/',
            status_code=302,
            target_status_code=200)
