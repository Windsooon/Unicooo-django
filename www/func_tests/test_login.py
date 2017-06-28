from .base_tests import BaseTestStaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache


class LoginWebdriver(BaseTestStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = 'just_test'
        cls.email = 'just_test@test.com'
        cls.password = '123456saasdfasdf'
        cls.live_server_url = 'http://web:8081'
        super(LoginWebdriver, cls).setUpClass()

    def setUp(self):
        # using docker connect
        active = {'is_active': 1}
        self.user_object = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                options=active,
        )
        self.driver.get(self.live_server_url + '/login/')
        self.email_login = self.driver.find_element_by_id('email_login')
        self.password_login = self.driver.find_element_by_id('password_login')
        self.login_form = self.driver.find_element_by_class_name('login-form')
        self.submit_btn = self.driver.find_element_by_class_name('submit-btn')

    def tearDown(self):
        cache.delete("email_" + self.email)
        cache.delete("user_name_" + self.username)

    # @unittest.skip("demonstrating skipping")
    def test_login_form_in_middle(self):
        '''
        login succeed from /login/ url
        '''
        self.assertAlmostEqual(
            self.email_login.location['x'] + self.email_login.size['width']/2,
            self.driver.get_window_size()["width"]/2, delta=25
        )
        self.assertAlmostEqual(
            self.password_login.location['x'] +
            self.password_login.size['width']/2,
            self.driver.get_window_size()["width"]/2, delta=25
        )
        self.assertAlmostEqual(
            self.login_form.location['x'] + self.login_form.size['width']/2,
            self.driver.get_window_size()["width"]/2, delta=25
        )

    def test_login_successed(self):
        '''
        login succeed from /login/ url
        '''
        # submit the correct form
        self.email_login.send_keys(self.email)
        self.password_login.send_keys(self.password)
        self.submit_btn.click()
        # wait for the front page show up
        self.wait_element_url("front-matrix")
        self.check_user_authed()

    def test_login_wrong_email(self):
        self.email_login.send_keys('just_sddftest@test.com')
        self.password_login.send_keys(self.password)
        self.submit_btn.click()
        self.wait_element_text(
            'form-server-error-p', 'Email or password incorrect.', 'class')

    def test_login_wrong_password(self):
        self.email_login.send_keys(self.email)
        self.password_login.send_keys('ewrqewk233323')
        self.submit_btn.click()
        self.wait_element_text(
            'form-server-error-p', 'Email or password incorrect.', 'class')

    def test_login_empty(self):
        self.submit_btn.click()
        self.assert_equal_error_text(
            'email_login-error',
            'Please enter a valid email address.')
        self.assert_equal_error_text(
            'password_login-error',
            'Please enter your password.')
