from django.contrib.admin import AdminSite, sites, ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import _user_has_perm
from django.db.models.base import ModelBase
from django.db.models import Model, QuerySet
from django.forms import Media
from django.db.models.options import Options
from django.contrib.admin.helpers import ActionForm, AdminForm
from django.http.response import HttpResponseRedirectBase
import json

from django.core import serializers
from django.http.response import DjangoJSONEncoder
from django.forms.models import model_to_dict

class MyJsonEncoder(DjangoJSONEncoder):

    def default(self, o):

        if not o:
            return ''
        if isinstance(o, HttpResponseRedirectBase):
            return str(getattr(o, 'url', None) or '')
        if isinstance(o, (ActionForm, AdminForm)):
            return str(o)  # TODO made Form serializer, in reality initial, values, choices
        if isinstance(o, ChangeList):
            return serializers.serialize('json', o.result_list, fields='__all__')
            # return str(o)  # TODO made ChangeList serializer
        if isinstance(o, Model):
            return model_to_dict(o)  # In reality we dont need it, all in Form
        if isinstance(o, Options):
            return str(o)  # TODO made Option serializer
        if isinstance(o, Media):
            return str(o)  # In reality we dont need any media
        if isinstance(o, QuerySet):
            return serializers.serialize('json', o, fields='__all__')
        if isinstance(o, ModelBase):
            return f'{o._meta.app_label}.{o._meta.model_name}'
        if isinstance(o, type(dict().items())):
            return super().default({str(key): val for key, val in o})

        try:
            return super().default(o)
        except TypeError as serializer_error:
            return str(o)

class WpAdminSite(AdminSite):

    permission = 'auth.is_stock_manager'

    def has_permission(self, request):
        return super().has_permission(request) and request.user.has_perm(self.permission)

    site_title = 'I like django.contrib.admin'
    site_header = 'Hello Django Con'
    index_title = 'Hello Pycon'
    final_catch_all_view = False

    def admin_view(self, view, cacheable=False):

        def wrapper(func):
            def wrapped(*args, **kwargs):
                instance = getattr(func, '__self__', None)
                if isinstance(instance, ModelAdmin):
                    new_instance = type(instance)(instance.model, instance.admin_site)
                    return func.__func__(new_instance, *args, **kwargs)
                return func(*args, **kwargs)

            return wrapped

        return super().admin_view(wrapper(view), cacheable=False)

    def get_app_list(self, request, app_label=None):
        return list(self._build_app_dict(request, app_label).values())

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


default_admin = sites.site  # WpAdminSite(name='admin')


from django.http.response import JsonResponse

class TranslationAdminSite(WpAdminSite):

    def admin_view(self, *args, **kwargs):

        def wrapper(func):
            def wrapped(request, *args, **kwargs):
                response = func(request, *args, **kwargs)
                if self.is_ajax(request):
                    if 'text/javascript' not in response.headers.get('Content-Type', ''):
                        return JsonResponse(
                            getattr(response, 'context_data', None) or {'redirect': response},
                            status=response.status_code, encoder=MyJsonEncoder)
                return response
            return wrapped
        return wrapper(super().admin_view(*args, **kwargs))

    permission = 'auth.is_translator'

translation_admin = TranslationAdminSite(name='translation-admin')


