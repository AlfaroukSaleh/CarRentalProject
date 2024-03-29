from django.urls import path
from . import views


app_name = "CarRental"
urlpatterns = [
    path("", views.index, name="index"),
    path("adduserindividual", views.adduserindividual,
         name="adduserindividual"),  # used to add individual users
    path("addusercorporate", views.addusercorporate,
         name="addusercorporate"),  # used to add corporate users
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("makereservation", views.makereservation, name="makereservation"),
    path("payment/<int:reservation_id>", views.payment, name="payment"),
    path("invoice/<int:payment_id>", views.invoice, name="invoice")


]
