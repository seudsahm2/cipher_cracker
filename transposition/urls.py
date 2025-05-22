from django.urls import path
from . import views

urlpatterns = [
    path('', views.transposition_view, name='transposition'),
]