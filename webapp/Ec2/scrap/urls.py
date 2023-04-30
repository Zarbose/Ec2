from django.urls import path
from scrap.views import index
from scrap.views import grafana
from scrap.views import get_name
from scrap.views import scenario_delete

urlpatterns = [
    path('', index, name="scrap-index"),
    path('grafana/', grafana, name="scrap-grafana"),
    path('get_name/', get_name, name="scrap-test"),
    path('scenario_delete/<int:id>/', scenario_delete, name="scrap-delete"),
]