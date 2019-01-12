from unittest import TestCase
from unittest.mock import patch


with patch('logging.basicConfig') as mocked_bc:
    with patch('configparser.ConfigParser') as mocked_cp:
        with patch('template.Template') as mocked_template:
            from chatcommands.slots import Slots


class TestSlots(TestCase):
    def test_do_work(self):
        self.fail()

    def test_spin_reels(self, mocked_get_all_data):
        mocked_get_all_data.return_value = {"Kappa": 1, "OpieOP": 2, "DansGame": 3}
        tmp = self.my_slots.spin_reels()
        print(tmp)

    @patch('template.Template.get_all_data')

    def setUp(self):
        self.user = "test-user"
        self.my_slots = Slots(self.user, "", "")

    def tearDown(self):
        del self.user
        del self.my_slots
