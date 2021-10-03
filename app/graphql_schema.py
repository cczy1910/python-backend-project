from graphene import Field
from graphene.types.scalars import Float, Int
from graphene.types.structures import List
from graphene import ObjectType, String

from app.models import Category, Item
import app.items as Items
import app.categories as Categories


class ItemQuery(ObjectType):
    id = Int()
    name = String()
    description = String()
    price = Float()


class CategoryQuery(ObjectType):
    id = Int()
    name = String()
    subcategories = List('app.graphql_schema.CategoryQuery')
    items = List(ItemQuery)

    def resolve_subcategories(parent, info):
        return list(map(
            convertCategory,
            Categories.getSubcategories(parent.id)
        ))

    def resolve_items(parent, info):
        return list(map(
            convertItem,
            Items.getItemsByCategory(parent.id)
        ))


class Query(ObjectType):
    category = Field(CategoryQuery, id=Int(default_value=1))

    def resolve_category(parent, info, id):
        return convertCategory(Categories.getCategory(id))


def convertItem(item: Item):
    return ItemQuery(
        id=item.id,
        name=item.name,
        description=item.name,
        price=item.price,
    )


def convertCategory(category: Category):
    return CategoryQuery(
        id=category.id,
        name=category.name,
    )
