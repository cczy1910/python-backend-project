from typing import List, Optional

from app.models import Item
import app.categories as Catgories
import app.data.data_access as DataAccess


def addItem(item: Item):
    items = DataAccess.loadItems()
    if (item.id in items):
        raise BaseException
    if (not item.category is None and Catgories.getCategory(item.category) is None):
        raise BaseException
    items[item.id] = item
    DataAccess.dumpItems(items)


def getItem(id: int) -> Optional[Item]:
    items = DataAccess.loadItems()
    return items.get(id)


def getItemsByCategory(category_id: int) -> List[Item]:
    def categoryMatches(item: Item):
        return item.category == category_id

    items = DataAccess.loadItems()
    return list(filter(
        categoryMatches,
        items.values()
    ))
