from tests.unit.unit_base_test import UnitBaseTest

from models.item import ItemModel

class TestItem(UnitBaseTest):
    def setUp(self):
        self.item = ItemModel('test', 19.99, 1)

    def test_create_item(self):
        self.assertEqual(self.item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(self.item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertEqual(self.item.store_id, 1,
                         "The store_id of the item after creation does not equal the constructor argument.")

    def test_item_json(self):
        expected_json = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(
            self.item.json(), expected_json,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(self.item.json(), expected_json))
