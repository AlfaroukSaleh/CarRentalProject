from django.urls import path
from . import views


app_name = "CarRental"
url_patterns = [
    path("", views.index, name="index")
]
