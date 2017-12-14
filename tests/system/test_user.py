import json
from models.user import UserModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('register', data={'username': 'hyndsenberg', 'password': 'password1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('hyndsenberg'))
                self.assertDictEqual(json.loads(response.data), {'message': 'User created successfully.'})

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('register', data={'username': 'hyndsenberg', 'password': 'password1234'})
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'hyndsenberg', 'password': 'password1234'}),
                                           headers={'Content-Type': 'application/json'})

                self.assertEqual(auth_response.status_code, 200)
                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('register', data={'username': 'hyndsenberg', 'password': 'password1234'})
                response = client.post('register', data={'username': 'hyndsenberg', 'password': 'password1234'})

                self.assertEqual(response.status_code, 400)
                self.assertIsNotNone(UserModel.find_by_username('hyndsenberg'))
                self.assertDictEqual(json.loads(response.data), {'message': 'A user with that username already exists'})