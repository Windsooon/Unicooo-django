import datetime
from django.test import TestCase
from activities.models import Act


class ActTestCase(TestCase):
    def setUp(self):
        Act.objects.create(
                act_title="test_title",
                act_content="test_content",
                act_thumb_url="145749729270df47ebce96cc7bd \
                               661f788786d51c16afce068",
                act_ident=10023,
                act_type=1,
                act_licence=1,
                act_star=0,
                act_status=0,
                act_url="/act/Windson/asdfasdfasf",
                act_delete=0,
                act_create_time=datetime.datetime.now(),
                user_id=100,
        )

    def test_act_can_create(self):
        test_act = Act.objects.get(act_title="test_title")
        self.assertEqual(test_act.act_content, "test_content")

    def test_act_can_modify(self):
        test_act = Act.objects.get(act_title="test_title")
        test_act.act_type = 2
        test_act.act_status = 1
        self.assertEqual(test_act.act_status, 1)
        self.assertEqual(test_act.act_type, 2)
