from unittest import TestCase
from unittest.mock import patch


with patch('logging.basicConfig') as mocked_bc:
    with patch('configparser.ConfigParser') as mocked_cp:
        with patch('template.Template') as mocked_template:
            from chatcommands.slots import Slots


class TestSlots(TestCase):
    def test_do_work(self):
        self.fail()

    def test_spin_reels(self):
        tmp = self.my_slots.spin_reels()
        print(tmp)

    def setUp(self):
        self.user = "test-user"
        self.my_slots = Slots(self.user, "", "")

    def tearDown(self):
        del self.user
        del self.my_slots
