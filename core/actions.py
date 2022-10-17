from django.contrib.admin import ModelAdmin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.utils.decorators import classonlymethod

from django.views.generic import FormView, View

class ActionView(View):

    def setup(self, admin, request, queryset, *args, **kwargs):
        vars(self).update(admin=admin, model=admin.model, queryset=queryset)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, admin, request, queryset, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.processing(*args, **kwargs)
        return None

    def processing(self, *args, **kwargs):
        for obj in self.queryset:
            self.process(obj)
            logger(f'{obj} successfully activated')
        message(self.request, _('all objects are active'))

    def process(self, obj):
        return obj

    @classonlymethod
    def as_view(cls, **initkwargs):
        response = super().as_view(**initkwargs)
        response.__name__ = cls.__name__
        response.short_description = ModelAdmin._get_action_description(cls, response.__name__)
        response.action_class = cls
        return response


def actionwrapper(cls, **initkwargs):
    return type(cls.__name__, (ActionViewMixIn, cls), {}).as_view(**initkwargs)


class ActivateActionView(ActionView):

    def processing(self, *args, **kwargs):
        for obj in self.queryset:
            obj.activate = True
            logger(f'{obj} successfully activated')
        message(self.request, _('all objects are active'))

    @classmethod
    def patch_request_data(cls, data):
        if cls.allow_empty and not data.getlist(ACTION_CHECKBOX_NAME):
            data._mutable = True
            data[ACTION_CHECKBOX_NAME] = '-1'
            data._mutable = False
        return data

    # def get_form(self, form_class=None, **kwargs):
    #     form = super(ActionView, self).get_form(form_class)
    #     form.request = self.request
    #     if hasattr(form, 'setup'):
    #         return form.setup(request=self.request, **dict({'prefix': self.get_prefix()}, **kwargs))
    #     return form

    @classmethod
    def check_permissions(cls, request, admin=None):
        return request.user.is_superuser or not getattr(cls, 'permissions', None) or (
            request.user.has_perms(permission.format(model_name=admin.opts.model_name, app_label=admin.opts.app_label) for permission in cls.permissions))


class ActionViewsMixin:

    def changelist_view(self, request, extra_context=None):
        data = request.POST.getlist('action') and request.POST
        if all(data, not data.get('_save'), not data.getlist(ACTION_CHECKBOX_NAME)):
            action_name = data.getlist('action')[int(data.get('index') or 0)]
            action, *_ = self.get_actions(request).get(action_name) or (None, )
            if action and getattr(action, 'allow_empty', None):
                data._mutable = True
                data[ACTION_CHECKBOX_NAME] = '-1'
                data._mutable = False
        return super().changelist_view(request, extra_context)

    def _filter_actions_by_permissions(self, request, actions):

        actions = (action for action in actions if any(
            not hasattr(action[0], 'permissions'),
            request.user.has_perms(action[0].permissions)))

        return super()._filter_actions_by_permissions(request, actions)


class EmptyAction(View):
    allow_empty = True
    short_description = 'empty action'
