from django.contrib.auth import get_user_model
from activities.models import Act
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_tests import BaseTestStaticLiveServerTestCase


class VisitFronePageWebdriver(BaseTestStaticLiveServerTestCase):

    def setUp(self):
        self.driver.get(self.live_server_url + '/')

    def tearDown(self):
        pass

    def test_search_correct(self):
        '''
        search return act_details
        '''
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
        self.act_title = 'just a test title'
        self.act_content = 'just a test content, content'
        self.act_thumb_url = '147326964570df47ebce96cc7' + \
                             'bd661f788786d51c16afce068'
        self.act_type = 2
        self.act = Act.objects.create(
            user=self.user,
            act_title=self.act_title,
            act_content=self.act_content,
            act_thumb_url=self.act_thumb_url,
            act_type=self.act_type,
            act_ident=10,
            act_url=self.username + '/' + self.act_title,
            )
        self.assertEqual(Act.objects.count(), 1)

        self.driver.get(self.live_server_url + '/')
        act_title = self.driver.find_element_by_class_name('act-title-p').text
        self.assertIn('just a test title', act_title)
        act_search = self.driver.find_element_by_class_name('act-search-text')
        act_search.send_keys(self.act.id+10000)
        self.driver.find_element_by_class_name(
            'act-search').send_keys(Keys.ENTER)
        self.wait_element_url(
            "activity-details-thumb", 'class',
            url=self.live_server_url + '/act/' +
            self.username + '/' + 'just%20a%20test%20title'
            )

    def test_search_no_activity(self):
        '''
        search return nothing
        '''
        self.driver.find_element_by_class_name(
            'act-search-text').send_keys(10080)
        self.driver.find_element_by_class_name(
            'act-search').click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.alert_is_present(), 'timeout'
            )
        finally:
            alert = self.driver.switch_to_alert()
            self.assertEqual(alert.text, 'Can\'t find this activity')
