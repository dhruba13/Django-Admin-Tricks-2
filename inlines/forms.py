from django import forms
from django.contrib.admin.models import LogEntry
from settings import default_translator as _

class ShopAdminForm(forms.ModelForm):

    _updated = forms.CharField(max_length=50, required=False, widget=forms.HiddenInput())

    def clean__updated(self):
        data = self.cleaned_data['_updated']
        if self.instance.pk and data != f'{self.instance.logs.first()!r}':
            self.add_error('__all__', forms.ValidationError(_('This object was changed in this time')))
        return data
