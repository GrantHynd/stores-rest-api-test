from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class TestStore(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('Corner Shop')
        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('Corner Shop')

            self.assertIsNone(StoreModel.find_by_name(store.name))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name(store.name))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name(store.name))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Corner Shop')
            store.save_to_db()
            ItemModel('Mars Bar', 0.75, 1).save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'Mars Bar')

    def test_json_with_no_items(self):
        with self.app_context():
            store = StoreModel('Corner Shop')
            store.save_to_db()
            expected_json = {'id': 1, 'name': 'Corner Shop', 'items': []}
            self.assertDictEqual(store.json(), expected_json)

    def test_json_with_items(self):
        with self.app_context():
            store = StoreModel('Corner Shop')
            store.save_to_db()

            ItemModel('Mars Bar', 0.75, 1).save_to_db()
            ItemModel('Twirl', 0.80, 1).save_to_db()

            expected_json = {
                'id': 1,
                'name': 'Corner Shop',
                'items': [
                    {
                        'name': 'Mars Bar',
                        'price': 0.75,
                    },
                    {
                        'name': 'Twirl',
                        'price': 0.80,
                    }
                ],
            }
            self.assertDictEqual(store.json(), expected_json)