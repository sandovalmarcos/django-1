from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def acerca(request):
    return HttpResponse("Acerca de")
def contacto(request):
    return HttpResponse("Contacto")
def home(request):
    return render(request, "recipes/pages/home.html", context= {
        "name" : "Habitación 1",
    })

