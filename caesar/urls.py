from django.urls import path
from . import views

app_name = "caesar"

urlpatterns = [
    path('', views.home, name='home'),
]
