from django.urls import path
from .views import index
from .views import test
from .views import get_name

urlpatterns = [
    path('', index, name="scrap-index"),
    path('test/', test, name="scrap-test"),
    path('get_name/', get_name, name="scrap-test"),
]