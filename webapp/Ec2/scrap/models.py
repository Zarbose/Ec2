from django.db import models
# from models import Scenario
from django.forms import ModelForm

WATT_CHOICES =(
    (1, "W"),
    (2, "KW"),
    (3, "MW"),
    (4, "GW"),
    (5, "TW"),
)

WATTH_CHOICES =(
    (1, "Wh"),
    (2, "KWh"),
    (3, "MWh"),
    (4, "GWh"),
    (5, "TWh"),
)

TIME_CHOICES =(
    (1, "Heure"),
    (2, "Minute"),
    (3, "Seconde"),
)

class Scenario(models.Model):

    asc_consomation = models.CharField(max_length=100)
    asc_consomation_choices = models.IntegerField(choices=WATT_CHOICES,default="1")
    
    asc_tmp_min = models.CharField(max_length=100)
    asc_tmp_min_choices = models.IntegerField(choices=TIME_CHOICES,default="1")

    asc_capa_max = models.CharField(max_length=100)
    asc_capa_max_choices = models.IntegerField(choices=WATTH_CHOICES,default="1")

    asc_capa_actu  = models.CharField(max_length=100)
    asc_capa_actu_choices  = models.IntegerField(choices=WATTH_CHOICES,default="1")


    desc_consomation = models.CharField(max_length=100)
    desc_consomation_choices = models.IntegerField(choices=WATT_CHOICES,default="1")

    desc_capa_max = models.CharField(max_length=100)
    desc_capa_max_choices = models.IntegerField(choices=WATTH_CHOICES,default="1")

    desc_capa_actu  = models.CharField(max_length=100)
    desc_capa_actu_choices  = models.IntegerField(choices=WATTH_CHOICES,default="1")

    target  = models.CharField(max_length=100)
    target_choices  = models.IntegerField(choices=WATTH_CHOICES,default="1")

    titre  = models.CharField(max_length=100)



