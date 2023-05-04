from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watch/<slug:videolink>", views.watch, name="watch"),
    path("premier_league/<str:videolink>", views.premier_league, name="premier_league"),
    path("coming_soon", views.coming_soon, name="coming_soon"),
]
