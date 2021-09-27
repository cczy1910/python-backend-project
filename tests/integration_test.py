from hashlib import md5
from unittest import TestCase
from unittest.mock import Mock, patch

from app.models import Credentials, Item, RegisterForm, User
import app.items as Items
import app.users as Users
import app.discounts as Discounts
import app.data.data_access as DataAccess


class IntegrationTest(TestCase):
    @patch('app.data.data_access.getItemsFile')
    @patch('app.data.data_access.getUsersFile')
    def setUp(self, getUsersFileMock: Mock, getItemsFileMock: Mock) -> None:
        getUsersFileMock.return_value = "tests/users.pickle"
        getItemsFileMock.return_value = "tests/items.pickle"
        DataAccess.initialize()

    @patch('app.data.data_access.getItemsFile')
    @patch('app.data.data_access.getUsersFile')
    def test_items(self, getUsersFileMock: Mock, getItemsFileMock: Mock):
        getUsersFileMock.return_value = "tests/users.pickle"
        getItemsFileMock.return_value = "tests/items.pickle"

        item_1 = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        item_2 = Item(
            id=2,
            name="another",
            description="desc2",
            price=400,
        )
        Items.addItem(item_1)
        self.assertEqual(item_1, Items.getItem(1))
        self.assertIsNone(Items.getItem(2))

        Items.addItem(item_2)
        self.assertEqual(item_1, Items.getItem(1))
        self.assertEqual(item_2, Items.getItem(2))

    @patch('app.data.data_access.getItemsFile')
    @patch('app.data.data_access.getUsersFile')
    def test_users(self, getUsersFileMock: Mock, getItemsFileMock: Mock):
        getUsersFileMock.return_value = "tests/users.pickle"
        getItemsFileMock.return_value = "tests/items.pickle"

        credentials_1 = Credentials(
            username="alice",
            password="pass"
        )
        register_form_1 = RegisterForm(
            id=1,
            credentials=credentials_1
        )
        credentials_2 = Credentials(
            username="bob",
            password="1234"
        )
        register_form_2 = RegisterForm(
            id=2,
            credentials=credentials_2
        )
        user_1 = User(
            id=1,
            username="alice",
            password_hash=str(md5(bytearray("pass", 'utf-8')).hexdigest()),
            discount=None,
        )
        user_2 = User(
            id=2,
            username="bob",
            password_hash=str(md5(bytearray("1234", 'utf-8')).hexdigest()),
            discount=None,
        )

        Users.register(register_form_1)
        self.assertEqual(user_1, Users.getUser(1))
        self.assertIsNone(Users.getUser(2))
        self.assertEqual(user_1, Users.authorize(credentials_1))
        self.assertIsNone(Users.authorize(Credentials(
            username="alice",
            password="wrong"
        )))

        Users.register(register_form_2)
        self.assertEqual(user_1, Users.authorize(credentials_1))
        self.assertEqual(user_2, Users.authorize(credentials_2))
        self.assertEqual(user_1, Users.getUser(1))
        self.assertEqual(user_2, Users.getUser(2))

    @patch('app.data.data_access.getItemsFile')
    @patch('app.data.data_access.getUsersFile')
    def test_users_discount(self, getUsersFileMock: Mock, getItemsFileMock: Mock):
        getUsersFileMock.return_value = "tests/users.pickle"
        getItemsFileMock.return_value = "tests/items.pickle"

        credentials_1 = Credentials(
            username="alice",
            password="pass"
        )
        register_form_1 = RegisterForm(
            id=1,
            credentials=credentials_1
        )

        Users.register(register_form_1)
        Users.setDiscount(1, 0.33)
        self.assertEqual(0.33, Users.authorize(credentials_1).discount)

        Users.setDiscount(1, 0.123)
        self.assertEqual(0.123, Users.authorize(credentials_1).discount)

    @patch('app.data.data_access.getItemsFile')
    @patch('app.data.data_access.getUsersFile')
    def test_discounts(self, getUsersFileMock: Mock, getItemsFileMock: Mock):
        getUsersFileMock.return_value = "tests/users.pickle"
        getItemsFileMock.return_value = "tests/items.pickle"

        credentials_1 = Credentials(
            username="alice",
            password="pass"
        )
        register_form_1 = RegisterForm(
            id=1,
            credentials=credentials_1
        )
        item_1 = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        item_2 = Item(
            id=2,
            name="another",
            description="desc2",
            price=400,
        )

        Users.register(register_form_1)
        Items.addItem(item_1)
        Items.addItem(item_2)
        self.assertEqual(item_1, Discounts.getDiscounted(credentials_1, 1))
        self.assertEqual(item_2, Discounts.getDiscounted(credentials_1, 2))
        self.assertIsNone(Discounts.getDiscounted(credentials_1, 3))
        with self.assertRaises(BaseException):
            Discounts.getDiscounted(Credentials(
                username="alice", password="wrong"), 1)

        Users.setDiscount(1, 0.5)
        self.assertEqual(
            Item(
                id=item_1.id,
                name=item_1.name + " (Скидка)",
                description=item_1.description,
                price=item_1.price * 0.5,
            ),
            Discounts.getDiscounted(credentials_1, 1)
        )
        self.assertEqual(
            Item(
                id=item_2.id,
                name=item_2.name + " (Скидка)",
                description=item_2.description,
                price=item_2.price * 0.5,
            ),
            Discounts.getDiscounted(credentials_1, 2)
        )
        self.assertIsNone(Discounts.getDiscounted(credentials_1, 3))
        with self.assertRaises(BaseException):
            Discounts.getDiscounted(Credentials(
                username="alice", password="wrong"), 1)
