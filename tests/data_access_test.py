
import os
import pickle
from unittest.mock import Mock, patch
from unittest import TestCase

from app.models import Item
import app.data.data_access as DataAccess


class DataAccessTest(TestCase):
    @patch('app.data.data_access.getItemsFile')
    def test_initialize(self, getItemsFileMock: Mock):
        items_file = "tests/items.pickle"
        getItemsFileMock.return_value = items_file
        DataAccess.initialize()
        with open(items_file, 'rb') as f:
            self.assertEqual({}, pickle.load(f))
        os.remove(items_file)

    @patch('app.data.data_access.getItemsFile')
    def test_load(self, getItemsFileMock: Mock):
        items_file = "tests/items.pickle"
        getItemsFileMock.return_value = items_file
        item_to_load = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        with open(items_file, 'wb') as f:
            pickle.dump({1: item_to_load}, f)
        self.assertEqual({1: item_to_load}, DataAccess.loadItems())
        os.remove(items_file)

    @patch('app.data.data_access.getItemsFile')
    def test_load_multiple(self, getItemsFileMock: Mock):
        items_file = "tests/items.pickle"
        getItemsFileMock.return_value = items_file
        item_to_load_1 = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        item_to_load_2 = Item(
            id=2,
            name="another",
            description="desc2",
            price=400,
        )
        item_to_load_3 = Item(
            id=3,
            name="third",
            description="desc3",
            price=99.9,
        )
        with open(items_file, 'wb') as f:
            pickle.dump(
                {1: item_to_load_1, 2: item_to_load_2, 3: item_to_load_3}, f)
        self.assertEqual({1: item_to_load_1, 2: item_to_load_2,
                         3: item_to_load_3}, DataAccess.loadItems())
        os.remove(items_file)

    @patch('app.data.data_access.getItemsFile')
    def test_dump(self, getItemsFileMock: Mock):
        items_file = "tests/items.pickle"
        getItemsFileMock.return_value = items_file
        item_to_dump = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        DataAccess.dumpItems({1: item_to_dump})
        with open(items_file, 'rb') as f:
            self.assertEqual({1: item_to_dump}, pickle.load(f))
        os.remove(items_file)

    @patch('app.data.data_access.getItemsFile')
    def test_dump_multiple(self, getItemsFileMock: Mock):
        items_file = "tests/items.pickle"
        getItemsFileMock.return_value = items_file
        item_to_dump_1 = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        item_to_dump_2 = Item(
            id=2,
            name="another",
            description="desc2",
            price=400,
        )
        item_to_dump_3 = Item(
            id=3,
            name="third",
            description="desc3",
            price=99.9,
        )
        DataAccess.dumpItems(
            {1: item_to_dump_1, 2: item_to_dump_2, 3: item_to_dump_3})
        with open(items_file, 'rb') as f:
            self.assertEqual(
                {1: item_to_dump_1, 2: item_to_dump_2, 3: item_to_dump_3}, pickle.load(f))
        os.remove(items_file)

    @patch('app.data.data_access.getItemsFile')
    def test_dump_and_load(self, getItemsFileMock: Mock):
        items_file = "tests/items.pickle"
        getItemsFileMock.return_value = items_file
        item_to_dump_and_load = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        DataAccess.dumpItems({1: item_to_dump_and_load})
        self.assertEqual({1: item_to_dump_and_load}, (DataAccess.loadItems()))
        os.remove(items_file)
