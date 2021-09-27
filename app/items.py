from typing import Optional

from app.models import Item
import app.data.data_access as DataAccess


def addItem(item: Item):
    items = DataAccess.loadItems()
    if (item.id in items):
        raise BaseException
    items[item.id] = item
    DataAccess.dumpItems(items)


def getItem(id: int) -> Optional[Item]:
    items = DataAccess.loadItems()
    return items.get(id)
