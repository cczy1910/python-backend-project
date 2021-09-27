
from hashlib import md5
from unittest.mock import Mock, patch
from unittest import TestCase

from app.models import Credentials, RegisterForm, User
import app.users as Users


class GetUsersTest(TestCase):
    @patch('app.data.data_access.loadUsers')
    def test_get(self, loadUsersMock: Mock):
        user_to_get = User(
            id=1,
            username="alice",
            password_hash="hash",
            discount=None,
        )
        loadUsersMock.return_value = {1: user_to_get}
        self.assertEqual(user_to_get, Users.getUser(1))

    @patch('app.data.data_access.loadUsers')
    def test_get_multiple(self, loadUsersMock: Mock):
        user_to_get_1 = User(
            id=1,
            username="alice",
            password_hash="hash1",
            discount=None,
        )
        user_to_get_2 = User(
            id=2,
            username="bob",
            password_hash="hash2",
            discount=None,
        )
        user_to_get_3 = User(
            id=3,
            username="admin",
            password_hash="hash2",
            discount=None,
        )
        loadUsersMock.return_value = {
            1: user_to_get_1, 2: user_to_get_2, 3: user_to_get_3}
        self.assertEqual(user_to_get_1, Users.getUser(1))
        self.assertEqual(user_to_get_2, Users.getUser(2))
        self.assertEqual(user_to_get_3, Users.getUser(3))

    @patch('app.data.data_access.loadUsers')
    def test_get_nonexisting(self, loadUsersMock: Mock):
        loadUsersMock.return_value = {}
        self.assertEqual(None, Users.getUser(1))


class RegisterUserTest(TestCase):
    @patch('app.data.data_access.dumpUsers')
    @patch('app.data.data_access.loadUsers')
    def test_register(self, loadUsersMock: Mock, dumpUsersMock: Mock):
        loadUsersMock.return_value = {}
        register_form = RegisterForm(
            id=1,
            credentials=Credentials(
                username="alice",
                password="pass"
            )
        )
        user_to_add = User(
            id=1,
            username="alice",
            password_hash=str(md5(bytearray("pass", 'utf-8')).hexdigest()),
            discount=None,
        )
        Users.register(register_form)
        dumpUsersMock.assert_called_with({1: user_to_add})

    @patch('app.data.data_access.dumpUsers')
    @patch('app.data.data_access.loadUsers')
    def test_register_multiple(self, loadUsersMock: Mock, dumpUsersMock: Mock):
        loadUsersMock.return_value = {}
        register_form_1 = RegisterForm(
            id=1,
            credentials=Credentials(
                username="alice",
                password="pass"
            )
        )
        register_form_2 = RegisterForm(
            id=2,
            credentials=Credentials(
                username="bob",
                password="1234"
            )
        )
        register_form_3 = RegisterForm(
            id=3,
            credentials=Credentials(
                username="admin",
                password="admin"
            )
        )
        user_to_add_1 = User(
            id=1,
            username="alice",
            password_hash=str(md5(bytearray("pass", 'utf-8')).hexdigest()),
            discount=None,
        )
        user_to_add_2 = User(
            id=2,
            username="bob",
            password_hash=str(md5(bytearray("1234", 'utf-8')).hexdigest()),
            discount=None,
        )
        user_to_add_3 = User(
            id=3,
            username="admin",
            password_hash=str(md5(bytearray("admin", 'utf-8')).hexdigest()),
            discount=None,
        )
        Users.register(register_form_1)
        dumpUsersMock.assert_called_with({1: user_to_add_1})
        loadUsersMock.return_value = {1: user_to_add_1}
        Users.register(register_form_2)
        dumpUsersMock.assert_called_with({1: user_to_add_1, 2: user_to_add_2})
        loadUsersMock.return_value = {1: user_to_add_1, 2: user_to_add_2}
        Users.register(register_form_3)
        dumpUsersMock.assert_called_with(
            {1: user_to_add_1, 2: user_to_add_2, 3: user_to_add_3})


class AuthorizeUserTest(TestCase):
    @patch('app.data.data_access.loadUsers')
    def test_authorize(self, loadUsersMock: Mock):
        user_to_get = User(
            id=1,
            username="alice",
            password_hash=str(md5(bytearray("pass", 'utf-8')).hexdigest()),
            discount=None,
        )
        loadUsersMock.return_value = {1: user_to_get}
        self.assertEqual(user_to_get, Users.authorize(
            Credentials(username="alice", password="pass")))

    @patch('app.data.data_access.loadUsers')
    def test_wrong_pass(self, loadUsersMock: Mock):
        user_to_get = User(
            id=1,
            username="alice",
            password_hash=str(md5(bytearray("pass", 'utf-8')).hexdigest()),
            discount=None,
        )
        loadUsersMock.return_value = {1: user_to_get}
        self.assertEqual(None, Users.authorize(
            Credentials(username="alice", password="wrong")))


class SetDicsountTest(TestCase):
    @patch('app.data.data_access.dumpUsers')
    @patch('app.data.data_access.loadUsers')
    def test_set_discount(self, loadUsersMock: Mock, dumpUsersMock: Mock):
        user_to_get = User(
            id=1,
            username="alice",
            password_hash="hash",
            discount=None,
        )
        loadUsersMock.return_value = {1: user_to_get}
        Users.setDiscount(1, 0.5)
        dumpUsersMock.assert_called_with({1: User(
            id=1,
            username="alice",
            password_hash="hash",
            discount=0.5,
        )})
