from django import forms
from .models import Scenario

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

class Test(forms.Form):
    asc_consomation = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1270, ...','aria-label': 'asc_energie','autocomplete': 'off'}))
    asc_consomation_choices = forms.ChoiceField(choices = WATT_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))
    
    asc_tmp_min = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1.5, 300, ...','aria-label': 'asc_activation','autocomplete': 'off'}))
    asc_tmp_min_choices = forms.ChoiceField(choices = TIME_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    asc_capa_max = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'asc_maximum','autocomplete': 'off'}))
    asc_capa_max_choices = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    asc_capa_actu  = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'asc_maximum_actu','autocomplete': 'off'}))
    asc_capa_actu_choices  = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))


    desc_consomation = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1270, ...','aria-label': 'desc_energie','autocomplete': 'off'}))
    desc_consomation_choices = forms.ChoiceField(choices = WATT_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    desc_capa_max = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'desc_maximum','autocomplete': 'off'}))
    desc_capa_max_choices = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    desc_capa_actu  = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '100, 3000, ...','aria-label': 'desc_maximum_actu','autocomplete': 'off'}))
    desc_capa_actu_choices  = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

    titre  = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Scénario STEP 1','aria-label': 'obj_titre','autocomplete': 'off'}))

    target  = forms.FloatField(min_value=0,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '1270, ...','aria-label': 'obj_energie','autocomplete': 'off'}))
    target_choices  = forms.ChoiceField(choices = WATTH_CHOICES ,widget=forms.Select(attrs={'class': 'form-select','aria-label': 'unite'}))

class ScenarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        placeholder_1 = '1270, ...'
        placeholder_2 = '1.5, 100, 3000, ...'
        placeholder_3 = 'Scénario 1'

        self.fields['asc_consomation'].widget.attrs['placeholder'] = placeholder_1
        self.fields['asc_consomation'].widget.attrs['aria-label'] = 'asc_energie'
        self.fields['asc_consomation'].widget.attrs['autocomplete'] = 'off'

        self.fields['asc_tmp_min'].widget.attrs['placeholder'] = placeholder_2
        self.fields['asc_tmp_min'].widget.attrs['aria-label'] = 'asc_activation'
        self.fields['asc_tmp_min'].widget.attrs['autocomplete'] = 'off'

        self.fields['asc_capa_max'].widget.attrs['placeholder'] = placeholder_2
        self.fields['asc_capa_max'].widget.attrs['aria-label'] = 'asc_maximum'
        self.fields['asc_capa_max'].widget.attrs['autocomplete'] = 'off'

        self.fields['asc_capa_actu'].widget.attrs['placeholder'] = placeholder_2
        self.fields['asc_capa_actu'].widget.attrs['aria-label'] = 'asc_maximum_actu'
        self.fields['asc_capa_actu'].widget.attrs['autocomplete'] = 'off'


        self.fields['desc_consomation'].widget.attrs['placeholder'] = placeholder_2
        self.fields['desc_consomation'].widget.attrs['aria-label'] = 'desc_energie'
        self.fields['desc_consomation'].widget.attrs['autocomplete'] = 'off'

        self.fields['desc_capa_max'].widget.attrs['placeholder'] = placeholder_2
        self.fields['desc_capa_max'].widget.attrs['aria-label'] = 'desc_maximum'
        self.fields['desc_capa_max'].widget.attrs['autocomplete'] = 'off'

        self.fields['desc_capa_actu'].widget.attrs['placeholder'] = placeholder_2
        self.fields['desc_capa_actu'].widget.attrs['aria-label'] = 'desc_maximum_actu'
        self.fields['desc_capa_actu'].widget.attrs['autocomplete'] = 'off'


        self.fields['titre'].widget.attrs['placeholder'] = placeholder_3
        self.fields['titre'].widget.attrs['aria-label'] = 'obj_titre'
        self.fields['titre'].widget.attrs['autocomplete'] = 'off'

        self.fields['target'].widget.attrs['placeholder'] = placeholder_1
        self.fields['target'].widget.attrs['aria-label'] = 'obj_energie'
        self.fields['target'].widget.attrs['autocomplete'] = 'off'

        
    class Meta:
        model = Scenario
        fields = '__all__'