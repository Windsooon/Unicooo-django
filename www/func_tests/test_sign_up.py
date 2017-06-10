from django.contrib.auth import get_user_model
from django.core.cache import cache
from .base_tests import BaseTestStaticLiveServerTestCase


class SignUpLoginWebdriver(BaseTestStaticLiveServerTestCase):

    def setUp(self):
        # default user
        self.username = 'just_test'
        self.email = 'just_test@test.com'
        self.password = '123456saasdfasdf'
        # user info for signup
        self.signup_email = "test_signup@email.com"
        self.signup_username = "just__test_signup"
        self.signup_password = "signup_password"
        # using docker connect
        self.live_server_url = 'http://web:8081'
        active = {'is_active': 1}
        self.user_object = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                options=active,
        )
        self.driver.get(self.live_server_url + '/signup/')
        self.email_signup = self.driver.find_element_by_id(
            'email_signup')
        self.username_signup = self.driver.find_element_by_id(
            'username_signup')
        self.password_signup = self.driver.find_element_by_id(
            'password_signup')
        self.signup_form = self.driver.find_element_by_class_name(
            'signup-form')
        self.submit_btn = self.driver.find_element_by_class_name(
            'submit-btn')

    def tearDown(self):
        cache.delete("email_" + self.signup_email)
        cache.delete("user_name_" + self.signup_username)
        cache.delete("email_" + self.email)
        cache.delete("user_name_" + self.username)

    def test_without_cache_signup_email_or_username_exist(self):
        self.email_signup.send_keys(self.email)
        self.username_signup.send_keys(self.username)
        self.password_signup.send_keys(self.password)
        self.submit_btn.click()
        self.assert_equal_error_text(
            'username_signup-error',
            'This username had already been registered.')
        self.assert_equal_error_text(
            'email_signup-error',
            'This email had already been registered.')

    def test_singup_form_in_middle(self):
        self.assertAlmostEqual(
            self.email_signup.location['x'] +
            self.email_signup.size['width']/2,
            self.driver.get_window_size()["width"]/2, delta=25
        )
        self.assertAlmostEqual(
            self.username_signup.location['x'] +
            self.username_signup.size['width']/2,
            self.driver.get_window_size()["width"]/2, delta=25
        )
        self.assertAlmostEqual(
            self.password_signup.location['x'] +
            self.password_signup.size['width']/2,
            self.driver.get_window_size()["width"]/2, delta=25
        )
        self.assertAlmostEqual(
            self.signup_form.location['x'] +
            self.signup_form.size['width']/2,
            self.driver.get_window_size()["width"]/2, delta=25
        )

    def test_signup_successed(self):
        '''
        signup succeed from /signup/
        '''
        self.email_signup.send_keys(self.signup_email)
        self.username_signup.send_keys(self.signup_username)
        self.password_signup.send_keys(self.signup_password)
        self.submit_btn.click()
        # wait for the front page show up
        self.wait_element_url("front-matrix")
        self.check_user_authed()

    def test_signup_not_valid_email_error_text_appear(self):
        self.email_signup.send_keys('just_test')
        self.driver.find_element_by_class_name('submit-btn').click()
        self.assert_equal_error_text(
            'email_signup-error',
            'Please enter a valid email address.')

    # @unittest.skip("demonstrating skipping")
    def test_signup_error_text_appear(self):
        self.driver.find_element_by_class_name('submit-btn').click()
        self.assert_equal_error_text(
            'email_signup-error',
            'Please enter a valid email address.')
        self.assert_equal_error_text(
            'username_signup-error',
            'Please enter your username.')
        self.assert_equal_error_text(
            'password_signup-error',
            'Please enter your password.')
        # signup normally
        email_signup = self.driver.find_element_by_id('email_signup')
        username_signup = self.driver.find_element_by_id('username_signup')
        password_signup = self.driver.find_element_by_id('password_signup')
        email_signup.send_keys(self.signup_email)
        username_signup.send_keys(self.signup_username)
        password_signup.send_keys(self.signup_password)
        self.assert_equal_error_text(
            'email_signup-error',
            '')
        self.assert_equal_error_text(
            'username_signup-error',
            '')
        self.assert_equal_error_text(
            'password_signup-error',
            '')
        self.driver.find_element_by_class_name('submit-btn').click()
        self.wait_element_url("front-matrix")
        self.assertEqual(get_user_model().objects.count(), 2)
        self.check_user_authed()
