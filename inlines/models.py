from django.db.models import Model, CharField, ImageField, ForeignKey, CASCADE, DO_NOTHING, TextField
from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from settings import default_translator as _


class BaseModel(Model):
    class Meta:
        abstract = True
    title = CharField(max_length=255)
    description = TextField()
    images = GenericRelation('core.Image')

class Shop(BaseModel):
    owner = ForeignKey(User, on_delete=DO_NOTHING, blank=True, null=True)

class Product(BaseModel):
    shop = ForeignKey('Shop', on_delete=CASCADE)

class Image(BaseModel):
    src = ImageField('My image')
    content_type = ForeignKey(ContentType, on_delete=DO_NOTHING, blank=True, null=True)
    object_id = CharField(_('Sourced object id'), max_length=50, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

