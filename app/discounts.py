from typing import Optional

from app.models import Credentials, Item
import app.items as Items
import app.users as Users


def getDiscounted(credentilas: Credentials, itemId: int) -> Optional[Item]:
    user = Users.authorize(credentilas)
    if user is None:
        raise BaseException
    item = Items.getItem(itemId)
    if user.discount is None or item is None:
        return item
    else:
        return Item(
            id=item.id,
            name=item.name + " (Скидка)",
            description=item.description,
            price=item.price * user.discount,
            category=item.category,
        )
