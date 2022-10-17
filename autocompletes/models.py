from django.db.models import (
    Model, CharField, ImageField, ForeignKey, CASCADE, DO_NOTHING, TextField,
    ManyToManyField, Q, BooleanField, Manager
)
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from settings import default_translator as _


class ManyToManyDescriptor(ManyToManyDescriptor):
    def __get__(self, instance, cls=None):
        response = super().__get__(instance, cls=cls)
        if instance:
            return response.filter(self.field._limit_choices_to)
        return response

class ManyToManyField(ManyToManyField):

    def contribute_to_class(self, cls, name, *args, **kwargs):
        super().contribute_to_class(cls, name, *args, **kwargs)
        setattr(cls, self.name, ManyToManyDescriptor(self.remote_field, reverse=False))


class BaseModel(Model):
    class Meta:
        abstract = True
    title = CharField(max_length=255)
    description = TextField()
    images = GenericRelation('core.Image')

    def __str__(self):
        return f'{self.title or repr(self)}'


class Land(BaseModel):
    ...

class Region(BaseModel):
    land = ForeignKey('Land', on_delete=CASCADE)
    bio = BooleanField(_('Allow BIO products'), default=True, blank=True)

class Visibility(BaseModel):
    product = ForeignKey('Product', on_delete=CASCADE)
    region = ForeignKey('Region', on_delete=CASCADE)
    visibile = BooleanField(_('Visible'), default=True, blank=True)


class Product(BaseModel):
    land = ManyToManyField('Land')
    region = ManyToManyField('Region', through="VisibilityProxy", limit_choices_to=Q(bio=True))

class RegionProxyManager(Manager):
    def get_queryset(self):
        if hasattr(self, 'through'):
            field = getattr(self.source_field.related_model, self.prefetch_cache_name).field
            super().get_queryset().filter(field._limit_choices_to)
        return super().get_queryset()

class RegionProxy(Region):
    class Meta:
        proxy = True
    objects = RegionProxyManager()

class VisibilityProxy(Visibility):

    class Meta:
        proxy = True
        auto_created = True
