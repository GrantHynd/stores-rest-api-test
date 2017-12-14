from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


class TestUser(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('hyndsenberg', 'password1234')

        self.assertEqual(user.username, 'hyndsenberg')
        self.assertEqual(user.password, 'password1234')