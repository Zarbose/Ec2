from django.urls import path
from scrap.views import index
from scrap.views import grafana
from scrap.views import scenario_delete

urlpatterns = [
    path('', index, name="scrap-index"),
    path('scenario_delete/<int:id>/', scenario_delete, name="scrap-delete"),
]