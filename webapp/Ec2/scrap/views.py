from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from scrap.forms import ScenarioForm
from scrap.models import Scenario

def index(request):
    return render(request,"scrap/index.html")

def test(request):
    scenarios = Scenario.objects.all()
    context = {
        "scenarios": scenarios
    }
    return render(request,"scrap/test.html",context)

def get_name(request):

    if request.method == "POST":
        form = ScenarioForm(request.POST)

        if form.is_valid():

            scenario = Scenario()

            scenario.asc_consomation = form.cleaned_data['asc_consomation']
            scenario.asc_consomation_choices = form.cleaned_data['asc_consomation_choices']
            scenario.asc_tmp_min = form.cleaned_data['asc_tmp_min']
            scenario.asc_tmp_min_choices = form.cleaned_data['asc_tmp_min_choices']
            scenario.asc_capa_max = form.cleaned_data['asc_capa_max']
            scenario.asc_capa_max_choices = form.cleaned_data['asc_capa_max_choices']
            scenario.asc_capa_actu = form.cleaned_data['asc_capa_actu']
            scenario.asc_capa_actu_choices = form.cleaned_data['asc_capa_actu_choices']
            scenario.desc_consomation = form.cleaned_data['desc_consomation']
            scenario.desc_consomation_choices = form.cleaned_data['desc_consomation_choices']
            scenario.desc_capa_max = form.cleaned_data['desc_capa_max']
            scenario.desc_capa_max_choices = form.cleaned_data['desc_capa_max_choices']
            scenario.desc_capa_actu = form.cleaned_data['desc_capa_actu']
            scenario.desc_capa_actu_choices = form.cleaned_data['desc_capa_actu_choices']
            scenario.target = form.cleaned_data['target']
            scenario.target_choices = form.cleaned_data['target_choices']
            scenario.titre = form.cleaned_data['titre']

            scenario.save()

            # print(form.cleaned_data)
            # print(scenario.titre)

            return HttpResponseRedirect("/test/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ScenarioForm()

    scenarios = Scenario.objects.all()
    context = {
        "form": form,
        "scenarios": scenarios,
        "scenarios_lenght": scenarios.count()
        # "scenarios_lenght": 0
    }

    return render(request, "scrap/name.html", context)
