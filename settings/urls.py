# from admins.apps import AdminConfig
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.admin.sites import all_sites

urlpatterns = [
    path(f'{site.name}/', site.urls) for site in all_sites
]
# urlpatterns = AdminConfig.get_urls()

urlpatterns += [
    # path(f'{sites.site.name}/doc/', include('django.contrib.admindocs.urls')),
    path('core/', include('core.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.USE_I18N:
    from django.conf.urls.i18n import i18n_patterns
    urlpatterns = i18n_patterns(*urlpatterns)
