from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from pyvirtualdisplay import Display


class VisitPageWebdriver(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(VisitPageWebdriver, cls).setUpClass()
        cls.display = Display(visible=0, size=(1024, 800))
        cls.display.start()
        cls.driver = webdriver.Firefox(
            executable_path='/usr/src/app/selenium_sources/geckodriver')
        cls.driver.implicitly_wait(1)
        cls.driver.set_window_size(1024, 768)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.display.stop()
        super(VisitPageWebdriver, cls).tearDownClass()

    def setUp(self):
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

    def test_signup_success(self):
        '''
        signup succeed from /signup/
        '''
        self.driver.get(self.live_server_url + '/signup/')
        email_signup = self.driver.find_element_by_id('email_signup')
        username_signup = self.driver.find_element_by_id('username_signup')
        password_signup = self.driver.find_element_by_id('password_signup')
        signup_form = self.driver.find_element_by_class_name('signup-form')
        # the sign_up form in the middle of the screen
        self.assertAlmostEqual(
            signup_form.location['x'] + signup_form.size['width']/2,
            512, delta=25
        )
        # create a new user, submit the correct form
        email_signup.send_keys('just_for_test@email.com')
        username_signup.send_keys('just_for_test')
        password_signup.send_keys('just_for_password')
        self.driver.find_element_by_class_name('submit-btn').click()
        # wait for the front page show up
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')

    def test_signup_error_text_appear(self):
        self.driver.get(self.live_server_url + '/signup/')
        email_signup = self.driver.find_element_by_id('email_signup')
        username_signup = self.driver.find_element_by_id('username_signup')
        password_signup = self.driver.find_element_by_id('password_signup')
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
        email_signup.send_keys('just_for_test@email.com')
        username_signup.send_keys('just_for_test')
        password_signup.send_keys('just_password')
        email_error_text2 = email_signup_error.text
        username_error_text2 = username_signup_error.text
        password_error_text2 = password_signup_error.text
        self.assertEqual(
                email_error_text2, '')
        self.assertEqual(
                username_error_text2, '')
        self.assertEqual(
                password_error_text2, '')

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
        email_signup.clear()
        email_signup.send_keys('just_test@test.com')
        email_error_text2 = email_signup_error.text
        self.assertEqual(
                email_error_text2, 'Please enter a valid email address.')

    def test_login_success(self):
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

        # submit the correct form
        email_login.send_keys('just_test@test.com')
        password_login.send_keys('123456saasdfasdf')
        self.driver.find_element_by_class_name('submit-btn').click()
        # wait for the front page show up
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "front-matrix"))
            )
        finally:
            self.assertEqual(
                self.driver.current_url, self.live_server_url + '/')
