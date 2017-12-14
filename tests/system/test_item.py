from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
import json


class TestItem(BaseTest):

    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('hyndsenberg', 'password1234').save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'hyndsenberg', 'password': 'password1234'}),
                                            headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = 'JWT ' + auth_token

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop').save_to_db()
                response = client.post('/item/Mars Bar', data={'price': 0.75, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(json.loads(response.data), {'name': 'Mars Bar', 'price': 0.75})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop').save_to_db()
                ItemModel('Mars Bar', 0.75, 1).save_to_db()
                response = client.post('/item/Mars Bar', data={'price': 0.75, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data), {'message': "An item with name 'Mars Bar' already exists."})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop').save_to_db()
                response = client.put('/item/Mars Bar', data={'price': 0.75, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': 'Mars Bar', 'price': 0.75})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop').save_to_db()
                ItemModel('Mars Bar', 0.75, 1).save_to_db()
                response = client.put('/item/Mars Bar (updated)', data={'price': 1.10, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': 'Mars Bar (updated)', 'price': 1.10})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop').save_to_db()
                ItemModel('Mars Bar', 0.75, 1).save_to_db()

                response = client.delete('/item/Mars Bar')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'message': 'Item deleted'})

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop')
                ItemModel('Mars Bar', 0.75, 1).save_to_db()
                response = client.get('/item/Mars Bar')

                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data), {'message': 'Could not authorize. Did you include a valid authorization header?'})

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop').save_to_db()
                response = client.get('/item/Mars Bar', headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Item not found'})

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop')
                ItemModel('Mars Bar', 0.75, 1).save_to_db()
                response = client.get('/item/Mars Bar', headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 200)

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Corner Shop').save_to_db()
                ItemModel('Mars Bar', 0.75, 1).save_to_db()
                ItemModel('Twirl', 0.80, 1).save_to_db()
                response = client.get('/items', headers={'Authorization': self.access_token})

                expected_items =  {
                    'items': [
                        {
                            'name': 'Mars Bar',
                            'price': 0.75
                        },
                        {
                            'name': 'Twirl',
                            'price': 0.80
                        },
                    ]
                }
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected_items)