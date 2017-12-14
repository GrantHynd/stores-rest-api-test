from models.user import UserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('hyndsenberg', 'password1234')

            self.assertIsNone(UserModel.find_by_username('hyndsenberg'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('hyndsenberg'))
            self.assertIsNotNone(UserModel.find_by_id(1))