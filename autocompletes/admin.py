from django.contrib.admin import ModelAdmin
from django.db.models import Q
from django.urls import resolve
from django.forms.widgets import Select

class RegionAdmin(ModelAdmin):
    search_fields = 'title',
    list_filter = 'land',

    def get_search_results(self, request, queryset, search_term):
        if self.is_ajax(request):
            query = {filter: request.GET.get(filter) for filter in self.list_filter}
            queryset = queryset.filter(**query)
        return super().get_search_results(request, queryset, search_term)

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class LandAdmin(ModelAdmin):
    search_fields = 'title',

    def has_add_permission(self, request, obj=None):
        if request.path.endswith('/change/') or request.path.endswith('/add/'):
            if ':autocompletes_product_' in resolve(request.path).view_name:
                return False
        return super().has_change_permission(request, obj=obj)

class ProductAdmin(ModelAdmin):

    class Media:
        js = ('autocompletes/js/search.js',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'land':
            kwargs['widget'] = Select
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'land':
            field.widget.attrs.update({'onchange': 'search(this);', 'data-name': 'region'})
            field.widget.can_view_related = False
        return field

    fields = 'title', 'land', 'region'
    autocomplete_fields = 'land', 'region'
