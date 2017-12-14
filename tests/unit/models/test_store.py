from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest

class TestStore(UnitBaseTest):
    def setUp(self):
        self.store = StoreModel('Corner Shop')

    def test_store_init(self):
        self.assertEqual(self.store.name, 'Corner Shop')