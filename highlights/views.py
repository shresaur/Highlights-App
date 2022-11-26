from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, "highlights/index.html")


def playepisode(request):
    return render(request, "highlights/playepisode.html")

