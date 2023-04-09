from django import forms

# CharField

WATT_CHOICES =(
    ("1", "W"),
    ("2", "KW"),
    ("3", "MW"),
    ("4", "GW"),
    ("5", "TW"),
)

WATTH_CHOICES =(
    ("1", "W"),
    ("2", "KW"),
    ("3", "MW"),
    ("4", "GW"),
    ("5", "TW"),
)

TIME_CHOICES =(
    ("1", "Heure"),
    ("2", "Minute"),
    ("3", "Seconde"),
)

class NameForm(forms.Form):
    asc_consomation = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1270, ...','aria-label': 'asc_energie'}))
    asc_consomation_choices = forms.ChoiceField(choices = WATT_CHOICES) # ,widget=forms.TextInput(attrs={'class': 'form-select','aria-label': 'unite'})
    asc_tmp_min = forms.FloatField(min_value=0,required=True)
    asc_capa_max = forms.FloatField(min_value=0,required=True)
    asc_capa_actu  = forms.FloatField(min_value=0,required=True)

    desc_consomation = forms.FloatField(min_value=0,required=True)
    desc_capa_max = forms.FloatField(min_value=0,required=True)
    desc_capa_actu  = forms.FloatField(min_value=0,required=True)

    titre  = forms.CharField(max_length=50,required=False)
    target  = forms.FloatField(min_value=0,required=True)
    