
from os import times
from unittest.mock import Mock, patch
from unittest import TestCase

from app.models import Item
import app.items as Items


class GetItemsTest(TestCase):
    @patch('app.data.data_access.loadItems')
    def test_get(self, loadItemsMock: Mock):
        item_to_get = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        loadItemsMock.return_value = {1: item_to_get}
        self.assertEqual(item_to_get, Items.getItem(1))

    @patch('app.data.data_access.loadItems')
    def test_get_multiple(self, loadItemsMock: Mock):
        item_to_get_1 = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        item_to_get_2 = Item(
            id=2,
            name="another",
            description="desc2",
            price=400,
        )
        item_to_get_3 = Item(
            id=3,
            name="third",
            description="desc3",
            price=99.9,
        )
        loadItemsMock.return_value = {
            1: item_to_get_1,
            2: item_to_get_2,
            3: item_to_get_3,
        }
        self.assertEqual(item_to_get_1, Items.getItem(1))
        self.assertEqual(item_to_get_2, Items.getItem(2))
        self.assertEqual(item_to_get_3, Items.getItem(3))

    @patch('app.data.data_access.loadItems')
    def test_get_nonexisting(self, loadItemsMock: Mock):
        loadItemsMock.return_value = {}
        self.assertEqual(None, Items.getItem(1))


class AddItemsTest(TestCase):
    @patch('app.data.data_access.dumpItems')
    @patch('app.data.data_access.loadItems')
    def test_add(self, loadItemsMock: Mock, dumpItemsMock: Mock):
        loadItemsMock.return_value = {}
        item_to_add = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        Items.addItem(item_to_add)
        dumpItemsMock.assert_called_with({1: item_to_add})

    @patch('app.data.data_access.dumpItems')
    @patch('app.data.data_access.loadItems')
    def test_add_multiple(self, loadItemsMock: Mock, dumpItemsMock: Mock):
        loadItemsMock.return_value = {}
        item_to_add_1 = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        item_to_add_2 = Item(
            id=2,
            name="another",
            description="desc2",
            price=400,
        )
        item_to_add_3 = Item(
            id=3,
            name="third",
            description="desc3",
            price=99.9,
        )
        Items.addItem(item_to_add_1)
        dumpItemsMock.assert_called_with({1: item_to_add_1})
        loadItemsMock.return_value = {1: item_to_add_1}
        Items.addItem(item_to_add_2)
        dumpItemsMock.assert_called_with({1: item_to_add_1, 2: item_to_add_2})
        loadItemsMock.return_value = {1: item_to_add_1, 2: item_to_add_2}
        Items.addItem(item_to_add_3)
        dumpItemsMock.assert_called_with({1: item_to_add_1, 2: item_to_add_2, 3: item_to_add_3})

    @patch('app.data.data_access.loadItems')
    def test_add_existing(self, loadItemsMock: Mock):
        item_to_add = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        loadItemsMock.return_value = {
            1: item_to_add
        }
        with self.assertRaises(BaseException):
            Items.addItem(item_to_add)
