from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watch/<slug:video_link>", views.watch, name="watch"),
    path("sport_highlights/<str:sport>", views.sport_highlights, name="sport_highlights"),
    path("coming_soon", views.coming_soon, name="coming_soon"),
]
