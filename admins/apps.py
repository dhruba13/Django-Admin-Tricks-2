from django.apps import apps
from django.urls import path
from django.contrib.admin import apps as adminApps, sites

class AdminConfig(adminApps.AdminConfig):
    default_site = 'admins.sites.WpAdminSite'

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)
        site = sites.site  # chaged with multiply admin sites
        # site.name = 'not_admin'
        site._registry = {}  # remove old registrations

        for config in apps.get_app_configs():
            admins = getattr(config.module, 'admin', None)

            for model in config.get_models():  # excluded auto_created and swapped
                model_admin = getattr(admins, f'{model.__name__}Admin', None)

                if model_admin and not site.is_registered(model):
                    site.register(model, model_admin)

    @classmethod
    def get_urls(cls, *args, **kwargs):
        return [path(f'{site.name}/', site.urls) for site in sites.all_sites]
