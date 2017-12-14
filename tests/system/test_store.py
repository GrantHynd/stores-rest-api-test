from models.store import StoreModel
from tests.base_test import BaseTest
import json


class TestStore(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Corner Shop')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('Corner Shop'))
                self.assertDictEqual(json.loads(response.data), {'id': 1, 'name': 'Corner Shop', 'items': []})

    def test_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Corner Shop')
                response = client.post('/store/Corner Shop')

                self.assertEqual(response.status_code, 400)
                self.assertIsNotNone(StoreModel.find_by_name('Corner Shop'))
                self.assertDictEqual(json.loads(response.data), {'message': "A store with name 'Corner Shop' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Corner Shop')
                response = client.delete('store/Corner Shop')

                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('Corner Shop'))
                self.assertDictEqual(json.loads(response.data), {'message': 'Store deleted'})


    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Corner Shop')
                response = client.get('store/Corner Shop')

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('Corner Shop'))
                self.assertDictEqual(json.loads(response.data), {'id': 1, 'name': 'Corner Shop', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('store/Corner Shop')

                self.assertEqual(response.status_code, 404)
                self.assertIsNone(StoreModel.find_by_name('Corner Shop'))
                self.assertDictEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Corner Shop')
                client.post('item/Mars Bar', data={'price': 0.75, 'store_id': 1})
                client.post('item/Twirl', data={'price': 0.80, 'store_id': 1})
                response = client.get('store/Corner Shop')

                expected_items = [
                    {
                        'name': 'Mars Bar',
                        'price': 0.75,
                    },
                    {
                        'name': 'Twirl',
                        'price': 0.80,
                    },
                ]

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('Corner Shop'))
                self.assertDictEqual(json.loads(response.data), {'id': 1, 'name': 'Corner Shop', 'items': expected_items})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Corner Shop')
                client.post('store/Tesco')
                client.post('store/Asda')
                response = client.get('stores')

                expected_stores = {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'Corner Shop',
                            'items': []
                        },
                        {
                            'id': 2,
                            'name': 'Tesco',
                            'items': []
                        },
                        {
                            'id': 3,
                            'name': 'Asda',
                            'items': []
                        },
                    ]
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected_stores)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Corner Shop')
                client.post('item/Mars Bar', data={'price': 0.75, 'store_id': 1})
                client.post('item/Twirl', data={'price': 0.80, 'store_id': 1})

                client.post('store/Tesco')

                client.post('store/Asda')
                client.post('item/Red Jumper', data={'price': 9.99, 'store_id': 3})

                response = client.get('stores')

                expected_stores_with_items = {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'Corner Shop',
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
                        },
                        {
                            'id': 2,
                            'name': 'Tesco',
                            'items': []
                        },
                        {
                            'id': 3,
                            'name': 'Asda',
                            'items': [
                                {
                                    'name': 'Red Jumper',
                                    'price': 9.99
                                }
                            ]
                        },
                    ]
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected_stores_with_items)