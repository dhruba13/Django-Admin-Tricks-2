from django.views.generic import TemplateView, View
from django.http import HttpResponse
from .models import Shop

class CheckVariable(TemplateView):
    template_name = 'core/check_variables.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(*args, **kwargs) | {'opts': Shop._meta}


class FileView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('here your text to write in file', content_type='text/plain', headers={'Content-Disposition': 'attachment; filename=file.txt'})
