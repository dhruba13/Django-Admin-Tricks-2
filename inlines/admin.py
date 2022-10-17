from django.contrib.admin import ModelAdmin, action, register, TabularInline, StackedInline
from django.template.loader import get_template
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from .models import Image, Product


class ProductInline(StackedInline):

    def my_inline(self, obj=None):
        response = ProductAdmin(self.model, self.admin.admin_site).add_view(self.admin.request)
        inline = response.context_data['inline_admin_formsets'][0]
        context = self.admin.response.context_data | {'inline_admin_formset': inline}
        return get_template(inline.opts.template).render(context, self.admin.request)

    model = Product
    extra = 1
    fields = 'title', 'my_inline',  # 'description'
    readonly_fields = 'my_inline',


class ImageInline(GenericTabularInline):
    model = Image
    extra = 0

class ProductAdmin(ModelAdmin):
    inlines = ImageInline,

class ShopAdmin(ModelAdmin):

    def get_inline_instances(self, *args, **kwargs):
        for inline in super().get_inline_instances(*args, **kwargs):
            vars(inline).update(admin=self)
            yield inline

    def render_change_form(self, request, *args, **kwargs):
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response

    def my_inline(self, obj=None):
        context = self.response.context_data
        inline = context['inline_admin_formset'] = context['inline_admin_formsets'].pop()
        return get_template(inline.opts.template).render(context, self.request)


    list_display = 'title',
    fields = 'title', # 'my_inline', 'description'
    # readonly_fields = 'my_inline',
    inlines = ProductInline, # ImageInline


class ImageAdmin(ModelAdmin):
    ...


