from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from pyvirtualdisplay import Display


class SignUpLoginWebdriver(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(SignUpLoginWebdriver, cls).setUpClass()
        cls.display = Display(visible=0, size=(1024, 800))
        cls.display.start()
        cls.driver = webdriver.Firefox(
            executable_path='/usr/src/app/selenium_sources/geckodriver')
        cls.driver.set_window_size(1024, 768)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.display.stop()
        super(SignUpLoginWebdriver, cls).tearDownClass()

    def setUp(self):
        self.email = 'just_test@test.com'
        self.username = 'just_test'
        self.password = '123456saasdfasdf'
        active = {'is_active': 1}
        self.user_object = get_user_model().objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
                options=active,
            )

        self.signup_email = "just_for_test_sign@email.com"
        self.signup_username = "just_for_signup"
        self.signup_password = "signup_password"

    def tearDown(self):
        cache.delete("email_" + self.signup_email)
        cache.delete("user_name_" + self.signup_username)

    # @unittest.skip("demonstrating skipping")
    def test_singup_form_in_middle(self):
        '''
        signup succeed from /signup/
        '''
        self.driver.get(self.live_server_url + '/signup/')
        signup_form = self.driver.find_element_by_class_name('signup-form')
        # the sign_up form in the middle of the screen
        self.assertAlmostEqual(
            signup_form.location['x'] + signup_form.size['width']/2,
            512, delta=25
        )

    def test_signup_no_error_messages(self):
        '''
        signup succeed from /signup/
        '''
        self.driver.get(self.live_server_url + '/signup/')
        email_signup = self.driver.find_element_by_id('email_signup')
        username_signup = self.driver.find_element_by_id('username_signup')
        password_signup = self.driver.find_element_by_id('password_signup')

        # create a new user, submit the correct form
        email_signup.send_keys(self.signup_email)
        username_signup.send_keys(self.signup_username)
        password_signup.send_keys(self.signup_password)

        self.driver.find_element_by_class_name('submit-btn').click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')

    def test_signup_successed(self):
        '''
        signup succeed from /signup/
        '''
        self.driver.get(self.live_server_url + '/signup/')
        email_signup = self.driver.find_element_by_id('email_signup')
        username_signup = self.driver.find_element_by_id('username_signup')
        password_signup = self.driver.find_element_by_id('password_signup')

        # create a new user, submit the correct form
        email_signup.send_keys(self.signup_email)
        username_signup.send_keys(self.signup_username)
        password_signup.send_keys(self.signup_password)

        self.driver.find_element_by_class_name('submit-btn').click()
        # wait for the front page show up
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')

    # @unittest.skip("demonstrating skipping")
    def test_signup_error_text_appear(self):
        self.driver.get(self.live_server_url + '/signup/')
        # click sign up without enter text
        self.driver.find_element_by_class_name('submit-btn').click()
        email_signup_error = self.driver.find_element_by_id(
            'email_signup-error')
        username_signup_error = self.driver.find_element_by_id(
            'username_signup-error')
        password_signup_error = self.driver.find_element_by_id(
            'password_signup-error')
        email_error_text = email_signup_error.text
        username_error_text = username_signup_error.text
        password_error_text = password_signup_error.text
        self.assertEqual(
            email_error_text, 'Please enter a valid email address.')
        self.assertEqual(
            username_error_text, 'Please enter your username.')
        self.assertEqual(
            password_error_text, 'Please enter your password.')
        # signup normally
        email_signup = self.driver.find_element_by_id('email_signup')
        username_signup = self.driver.find_element_by_id('username_signup')
        password_signup = self.driver.find_element_by_id('password_signup')
        email_signup.send_keys(self.signup_email)
        username_signup.send_keys(self.signup_username)
        password_signup.send_keys(self.signup_password)
        email_error_text2 = email_signup_error.text
        username_error_text2 = username_signup_error.text
        password_error_text2 = password_signup_error.text
        self.assertEqual(
            email_error_text2, '')
        self.assertEqual(
            username_error_text2, '')
        self.assertEqual(
            password_error_text2, '')
        self.driver.find_element_by_class_name('submit-btn').click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')

    def test_signup_wrong_email_error_text_appear(self):
        self.driver.get(self.live_server_url + '/signup/')
        email_signup = self.driver.find_element_by_id('email_signup')
        email_signup.send_keys('just_for_test')
        self.driver.find_element_by_class_name('submit-btn').click()
        email_signup_error = self.driver.find_element_by_id(
            'email_signup-error')
        email_error_text = email_signup_error.text
        self.assertEqual(
            email_error_text, 'Please enter a valid email address.')

    def test_signup_already_registerd_email_error_text_appear(self):
        self.driver.get(self.live_server_url + '/signup/')
        email_signup = self.driver.find_element_by_id('email_signup')
        email_signup.send_keys('just_test@test.com')
        self.driver.find_element_by_class_name('submit-btn').click()
        email_signup_error = self.driver.find_element_by_id(
            'email_signup-error')
        email_error_text = email_signup_error.text
        self.assertEqual(
                email_error_text, 'This email had already been registered.')

    def test_signup_already_registerd_username_error_text_appear(self):
        self.driver.get(self.live_server_url + '/signup/')
        username_signup = self.driver.find_element_by_id('username_signup')
        username_signup.send_keys('just_test')
        self.driver.find_element_by_class_name('submit-btn').click()
        username_signup_error = self.driver.find_element_by_id(
            'username_signup-error')
        username_error_text = username_signup_error.text
        self.assertEqual(
            username_error_text, 'This username had already been registered.')

    # @unittest.skip("demonstrating skipping")
    def test_login_form_in_middle(self):
        '''
        login succeed from /login/ url
        '''
        self.driver.get(self.live_server_url + '/login/')
        email_login = self.driver.find_element_by_id('email_login')
        password_login = self.driver.find_element_by_id('password_login')
        login_form = self.driver.find_element_by_class_name('login-form')
        self.assertAlmostEqual(
            email_login.location['x'] + email_login.size['width']/2,
            512, delta=25
        )
        self.assertAlmostEqual(
            password_login.location['x'] + password_login.size['width']/2,
            512, delta=25
        )
        self.assertAlmostEqual(
            login_form.location['x'] + login_form.size['width']/2,
            512, delta=25
        )

    def test_login_successed(self):
        '''
        login succeed from /login/ url
        '''
        self.driver.get(self.live_server_url + '/login/')
        email_login = self.driver.find_element_by_id('email_login')
        password_login = self.driver.find_element_by_id('password_login')

        # submit the correct form
        email_login.send_keys(self.email)
        password_login.send_keys(self.password)
        self.driver.find_element_by_class_name('submit-btn').click()
        # wait for the front page show up
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')

    def test_login_wrong_email(self):
        self.driver.get(self.live_server_url + '/login/')
        email_login = self.driver.find_element_by_id('email_login')
        password_login = self.driver.find_element_by_id('password_login')

        # submit the correct form
        email_login.send_keys('just_sdftest@test.com')
        password_login.send_keys(self.password)
        self.driver.find_element_by_class_name('submit-btn').click()
        self.assertEqual(
            self.driver.current_url, self.live_server_url + '/login/?next=/')

    def test_login_wrong_password(self):
        self.driver.get(self.live_server_url + '/login/')
        email_login = self.driver.find_element_by_id('email_login')
        password_login = self.driver.find_element_by_id('password_login')

        # submit the correct form
        email_login.send_keys(self.email)
        password_login.send_keys('sdfasdfasdiuu')
        self.driver.find_element_by_class_name('submit-btn').click()
        self.assertEqual(
            self.driver.current_url, self.live_server_url + '/login/?next=/')