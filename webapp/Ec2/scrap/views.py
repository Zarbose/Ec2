from django.http import HttpResponseRedirect
from django.shortcuts import render
from scrap.forms import ScenarioForm
from scrap.models import Scenario
import os

def index(request):
    if request.method == "POST":
        if 'small_simuler' in request.POST:
            id = request.POST['small_simuler']
            return HttpResponseRedirect("/grafana/"+id)
        elif 'small_suprimer' in request.POST:
            id = request.POST['small_suprimer']
            return HttpResponseRedirect("/scenario_delete/"+id)

    if request.method == "POST":
        form = ScenarioForm(request.POST)
        if form.is_valid():

            print(form.cleaned_data)

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
            id = scenario.id

            return HttpResponseRedirect("/grafana/"+str(id))
    else:
        form = ScenarioForm()

    scenarios = Scenario.objects.all()
    context = {
        "form": form,
        "cur_scenario": 0,
        "scenarios": scenarios,
        "scenarios_lenght": scenarios.count()
        # "scenarios_lenght": 0
    }

    return render(request, "scrap/index.html", context)

def grafana(request,id):
    scenarios = Scenario.objects.all()
    context = {
        "id": id,
        "scenarios": scenarios
    }

    os.system("python3 /app/script/startup.py")

    return render(request,"scrap/simulation.html",context)

def scenario_delete(request, id):
    scenario = Scenario.objects.get(id=id)
    scenario.delete()

    return HttpResponseRedirect("/")
