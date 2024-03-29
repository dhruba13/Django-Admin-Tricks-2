from django import forms
from django.contrib.admin.models import LogEntry


class ShopAdminForm(forms.ModelForm):
    updated = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    _log_object = None

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.pk:
            self._log_object = LogEntry.objects.filter(object_id=instance.pk).first()
            kwargs['initial'] = kwargs.get('initial', {}) | {'updated': f'{self._log_object.action_time}'}
        super(ShopAdminForm, self).__init__(*args, **kwargs)

    def clean_updated(self):
        value = self.cleaned_data['updated']
        if self._log_object and value == f'{self._log_object.action_time}':
            return value
        raise forms.ValidationError('Error')


