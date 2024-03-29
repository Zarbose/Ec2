from django.http import HttpResponseRedirect
from django.shortcuts import render
from scrap.forms import ScenarioForm
from scrap.models import Scenario
from scrap.script import scrap as sc
import os
from django.shortcuts import redirect
from scrap.script import startup as st

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
            
            # print("AV SAVE")
            scenario.save()
            id = scenario.id
            # print("AP SAVE")
            return HttpResponseRedirect("/grafana/"+str(id))
    else:
        form = ScenarioForm()

    scenarios = Scenario.objects.all()
    context = {
        "form": form,
        "cur_scenario": 0,
        "scenarios": scenarios,
        "scenarios_lenght": scenarios.count()
    }

    return render(request, "scrap/index.html", context)

def grafana(request,id):
    # print("GRAFANA")
    scenarios = Scenario.objects.all()
    context = {
        "id": id,
        "scenarios": scenarios
    }
    sce = Scenario.objects.get(pk=id)
    sce=sce.__repr__()

    status_web = st.initDailyPrice()
    # print("WEB -------------- :",status_web)
    status_sim = sc.scrap_main(sce)
    # print("SIM -------------- :",status_sim)

    if status_web or status_sim == -1:
        Scenario.objects.get(pk=id).delete()
        return HttpResponseRedirect("/")

    return HttpResponseRedirect("/")

def scenario_delete(request, id):
    scenario = Scenario.objects.get(id=id)
    scenario.delete()

    return HttpResponseRedirect("/")
