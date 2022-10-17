from django.urls import path
from .views import CheckVariable, FileView


urlpatterns = [
    path('check/', CheckVariable.as_view()),
    path("create_file", FileView.as_view(), name="create_file"),
]
