import graphene

from graphene_django.types import DjangoObjectType

# from cookbook.ingredients.models import Category, Ingredient
#
#
# class CategoryType(DjangoObjectType):
#     class Meta:
#         model = Category
#
#
class StationType(graphene.ObjectType):
    pass
    # class Meta:
    #     model = Ingredient


class Query(object):
    all_stations = graphene.List(StationType)

    def resolve_active_stations(self, info, **kwargs):
        return []
