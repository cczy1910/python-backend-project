from typing import List, Optional

import app.data.data_access as DataAccess
from app.models import Category


def addCategory(category: Category):
    categories = DataAccess.loadCategories()
    if (category.id in categories):
        raise BaseException
    if (not category.parent_id is None and not category.parent_id in categories):
        raise BaseException
    categories[category.id] = category
    DataAccess.dumpCategories(categories)


def getCategory(id: int) -> Optional[Category]:
    categories = DataAccess.loadCategories()
    return categories.get(id)


def getSubcategories(category_id: Optional[int]) -> List[Category]:
    def categoryMatches(category: Category):
        return category.parent_id == category_id

    categories = DataAccess.loadCategories()
    return list(filter(
        categoryMatches,
        categories.values()
    ))
