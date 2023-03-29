from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, 'index.html')
    return render(request,'index.html')
    return HttpResponse("Hello, world. You're at the polls index.")

# def config_view(request):
#     return render(request,'scrap/views/index.html')
