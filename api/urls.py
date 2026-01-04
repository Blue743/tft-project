from django.urls import path
from .views import health_check
from . import views

urlpatterns = [
    path("health/", health_check),
    path("matches/", views.get_game)
]

