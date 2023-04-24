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
    ("1", "Wh"),
    ("2", "KWh"),
    ("3", "MWh"),
    ("4", "GWh"),
    ("5", "TWh"),
)

TIME_CHOICES =(
    ("1", "Heure"),
    ("2", "Minute"),
    ("3", "Seconde"),
)

class NameForm(forms.Form):
    asc_consomation = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1270, ...','aria-label': 'asc_energie'}))
    asc_consomation_choices = forms.ChoiceField(choices = WATT_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))
    
    asc_tmp_min = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1.5, 300, ...','aria-label': 'asc_activation'}))
    asc_tmp_min_choices = forms.ChoiceField(choices = TIME_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    asc_capa_max = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'asc_maximum'}))
    asc_capa_max_choices = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    asc_capa_actu  = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'asc_maximum_actu'}))
    asc_capa_actu_choices  = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))


    desc_consomation = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1270, ...','aria-label': 'desc_energie'}))
    desc_consomation_choices = forms.ChoiceField(choices = WATT_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    desc_capa_max = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'desc_maximum'}))
    desc_capa_max_choices = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    desc_capa_actu  = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'desc_maximum_actu'}))
    desc_capa_actu_choices  = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    titre  = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Scénario STEP 1','aria-label': 'obj_titre'}))

    target  = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1270, ...','aria-label': 'obj_energie'}))
    target_choices  = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))
    