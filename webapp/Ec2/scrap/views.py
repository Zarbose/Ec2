from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ScenarioForm

def index(request):
    return render(request,"scrap/index.html")

def test(request):
    return render(request,"scrap/test.html")

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ScenarioForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            print(form.cleaned_data)

            return HttpResponseRedirect("/test/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ScenarioForm()

    return render(request, "scrap/name.html", {"form": form})
