from typing import Optional
from hashlib import md5

from app.models import Credentials, RegisterForm, User
import app.data.data_access as DataAccess


def register(registerForm: RegisterForm):
    users = DataAccess.loadUsers()
    if (registerForm.id in users):
        raise BaseException
    users[registerForm.id] = User(
        id=registerForm.id,
        username=registerForm.credentials.username,
        password_hash=str(md5(bytearray(registerForm.credentials.password, 'utf-8')).hexdigest()),
        discount=None
    )
    DataAccess.dumpUsers(users)


def setDiscount(userId: int, discount: float):
    users = DataAccess.loadUsers()
    if (not userId in users):
        raise BaseException
    users[userId] = User(
        id=users[userId].id,
        username=users[userId].username,
        password_hash=users[userId].password_hash,
        discount=discount
    )
    DataAccess.dumpUsers(users)


def authorize(credentilas: Credentials) -> Optional[User]:
    users = DataAccess.loadUsers()
    for id in users.keys():
        if users[id].username == credentilas.username and users[id].password_hash == str(md5(bytearray(credentilas.password, 'utf-8')).hexdigest()):
            return users[id]
    return None

def getUser(id: int) -> Optional[User]:
    users = DataAccess.loadUsers()
    return users.get(id)
