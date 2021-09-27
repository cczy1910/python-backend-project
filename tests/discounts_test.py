from hashlib import md5
from unittest.mock import Mock, patch
from unittest import TestCase

from app.models import Credentials, Item, User
import app.discounts as Discounts


class GetDiscountedTest(TestCase):
    @patch('app.items.getItem')
    @patch('app.users.authorize')
    def test_get_discounted(self, authorizeMock: Mock, getItemMock: Mock):
        user_to_get = User(
            id=1,
            username="alice",
            password_hash=str(md5(bytearray("pass", 'utf-8')).hexdigest()),
            discount=0.5,
        )
        item_to_get = Item(
            id=1,
            name="tovar",
            description="desc",
            price=300,
        )
        authorizeMock.return_value = user_to_get
        getItemMock.return_value = item_to_get
        self.assertEqual(
            Item(
                id=item_to_get.id,
                name=item_to_get.name + " (Скидка)",
                description=item_to_get.description,
                price=item_to_get.price * user_to_get.discount,
            ),
            Discounts.getDiscounted(
                1,
                Credentials(username="alice", password="pass")
            )
        )
