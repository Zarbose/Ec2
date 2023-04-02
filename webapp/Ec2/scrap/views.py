from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse("<H1>L'app</H1>")
    return render(request,"scrap/index.html")
