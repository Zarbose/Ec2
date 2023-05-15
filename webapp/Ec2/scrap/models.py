from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators 

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

    asc_consomation = models.FloatField(max_length=100)
    asc_consomation_choices = models.IntegerField(choices=WATT_CHOICES,default="1")

    asc_capa_max = models.FloatField(max_length=100)
    asc_capa_max_choices = models.IntegerField(choices=WATTH_CHOICES,default="1")

    asc_capa_actu  = models.FloatField(max_length=100)
    asc_capa_actu_choices  = models.IntegerField(choices=WATTH_CHOICES,default="1")


    desc_consomation = models.FloatField(max_length=100)
    desc_consomation_choices = models.IntegerField(choices=WATT_CHOICES,default="1")

    desc_capa_max = models.FloatField(max_length=100)
    desc_capa_max_choices = models.IntegerField(choices=WATTH_CHOICES,default="1")

    desc_capa_actu  = models.FloatField(max_length=100)
    desc_capa_actu_choices  = models.IntegerField(choices=WATTH_CHOICES,default="1")

    target  = models.FloatField(max_length=100)
    target_choices  = models.IntegerField(choices=WATTH_CHOICES,default="1")

    titre  = models.CharField(max_length=100)

    def __repr__(self):
        string = {'asc_consomation': self.asc_consomation, 'asc_consomation_choices': self.asc_consomation_choices, 
                    'asc_capa_max': self.asc_capa_max, 'asc_capa_max_choices': self.asc_capa_max_choices, 
                    'asc_capa_actu': self.asc_capa_actu, 'asc_capa_actu_choices': self.asc_capa_actu_choices, 
                    'desc_consomation': self.desc_consomation, 'desc_consomation_choices': self.desc_consomation_choices, 
                    'desc_capa_max': self.desc_capa_max, 'desc_capa_max_choices': self.desc_capa_max_choices, 
                    'desc_capa_actu': self.desc_capa_actu, 'desc_capa_actu_choices': self.desc_capa_actu_choices, 
                    'target': self.target, 'target_choices': self.target_choices, 
                    'titre': self.titre}
        return string


