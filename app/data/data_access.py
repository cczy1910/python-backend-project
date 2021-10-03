from typing import Dict
import pickle

from app.models import Category, Item, User


def getItemsFile():
    return "app/data/items.pickle"


def getUsersFile():
    return "app/data/users.pickle"


def getCategoriesFile():
    return "app/data/categories.pickle"


def loadItems() -> Dict[int, Item]:
    with open(getItemsFile(), 'rb') as f:
        return pickle.load(f)


def dumpItems(items: Dict[int, Item]):
    with open(getItemsFile(), 'wb') as f:
        pickle.dump(items, f)


def loadUsers() -> Dict[int, User]:
    with open(getUsersFile(), 'rb') as f:
        return pickle.load(f)


def dumpUsers(users: Dict[int, User]):
    with open(getUsersFile(), 'wb') as f:
        pickle.dump(users, f)

def loadCategories() -> Dict[int, Category]:
    with open(getCategoriesFile(), 'rb') as f:
        return pickle.load(f)


def dumpCategories(categories: Dict[int, Category]):
    with open(getCategoriesFile(), 'wb') as f:
        pickle.dump(categories, f)

def initialize():
    with open(getItemsFile(), 'wb') as f1:
        pickle.dump({}, f1)
    with open(getUsersFile(), 'wb') as f2:
        pickle.dump({}, f2)
    with open(getCategoriesFile(), 'wb') as f2:
        pickle.dump({}, f2)
