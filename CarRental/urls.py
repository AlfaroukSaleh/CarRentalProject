from django.urls import path
from . import views


app_name = "CarRental"
urlpatterns = [
    path("", views.index, name="index"),
    path("adduserindividual", views.adduserindividual,
         name="adduserindividual"),  # used to add individual users
    path("addusercorporate", views.addusercorporate,
         name="addusercorporate"),  # used to add corporate users

]
