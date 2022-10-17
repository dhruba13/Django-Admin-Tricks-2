from django.contrib.admin import ModelAdmin, action, register
from django.contrib import admin
from admins.sites import translation_admin
from django.db.models import Count, Model, CharField

from core.models import Shop, Product, Image

from .actions import ActionViewsMixin, EmptyAction, actionwrapper

from django.template.loader import get_template

from .forms import ShopAdminForm


# Problem with function in ModelAdmin.get_fields(None) #Issue 33703: (closed: invalid)

# class MyModel(Model):

#     class Meta:
#         managed = False

#     title = CharField('Meta Title of object', max_length=80, blank=True)
#     slug = CharField('Meta Slug of object', max_length=80, blank=True)


# class MyModelAdmin1(ModelAdmin):
#     fields = ('title', )


# class MyModelAdmin2(ModelAdmin):
#     fieldset = ('title', )


# print(MyModelAdmin1(MyModel, None).get_fields(None))
# answer >>> ('title',)

# print(MyModelAdmin2(MyModel, None).get_fields(None))
# answer >>> ['title', 'slug']


@action(permissions=['stupid', 'view'], description='My Big Description')
def MyFunc(*args, **kwargs):
    """Empty func-based-Action."""
MyFunc.permissions = ('user.is_stock_manager',)
MyFunc.allow_empty = True


class ProductAdmin(ModelAdmin):
    actions = (MyFunc, EmptyAction.as_view())

    def has_stupid_permission(self, *args, **kwargs):
        return False

    list_display = ('__str__', 'shop',)
    list_editable = ('shop', )

    def _filter_actions_by_permissions(self, request, actions):
        actions = (action for action in actions if not hasattr(action[0], 'permissions') or request.user.has_perms(action[0].permissions))
        return super()._filter_actions_by_permissions(request, actions)


class ProductInline(admin.TabularInline):
    model = Product


# @admin.register(Shop, site=translation_admin)
class ShopAdmin(ModelAdmin):
    actions = (MyFunc, EmptyAction.as_view())
    list_display = ('title', 'product_count')
    fields = ('title', 'updated')
    inlines = ProductInline,
    form = ShopAdminForm

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).annotate(product_count=Count('product'))

    def product_count(self, obj, *args, **kwargs):
        return obj.product_count

    def has_stupid_permission(self, *args, **kwargs):
        return False


# ImageAdmin = type('ImageAdmin', (ModelAdmin,), {})

class ImageAdmin(ModelAdmin):
    """Admin clsss for Image modelModelAdmin"""

    def get_actions(self, request):
        return super().get_actions(request)

    def changeform_view(self, request, *args, **kwargs):
        self.request = request
        self.user = request.user
        return super().changeform_view(request, *args, **kwargs)
