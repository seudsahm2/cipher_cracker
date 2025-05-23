from django.urls import path
from . import views

app_name = "transposition"

urlpatterns = [
    path('', views.transposition_view, name='transposition'),
]