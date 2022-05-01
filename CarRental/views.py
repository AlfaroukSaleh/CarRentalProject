from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import hashlib
from itertools import chain
from .models import Individual_customer, Corporate_customer, Insurance_company
# Create your views here.


def index(request):
    return render(request, "CarRental/index.html")


def adduserindividual(request):  # used for adding Indivdual users
    if request.method == "GET":
        return render(request, "CarRental/adduserindividual.html")

    if request.user.is_authenticated:
        messages.error(request, "You are not authorized to view this page!")
        return HttpResponseRedirect(reverse("CarRental:index"))
    else:
        if request.method == "POST":

            # Checks if this email was previously used
            user_email_validator = Individual_customer.objects.filter(
                user_email=request.POST["user_email"]).first()
            if user_email_validator is not None:
                messages.error(request, "This email was previously used!")
                return HttpResponseRedirect(reverse("adduserindividual"))

                # Checks if this number was previously used
            user_phone_validator = Individual_customer.objects.filter(
                user_phone=request.POST["user_phone"]).first()

            if user_phone_validator is not None:
                messages.error(
                    request, "This phone number was previously used!")
                return HttpResponseRedirect(reverse("adduserindividual"))

            if request.POST["user_pass1"] != request.POST["user_pass2"]:
                messages.error(
                    request, "The two passwords don't match!")
                return HttpResponseRedirect(reverse("adduserindividual"))

                # Creates a new user
            user = Individual_customer(user_name=request.POST["user_name"], user_email=request.POST["user_email"], user_phone=request.POST[
                "user_phone"], user_password=hashlib.md5(request.POST["user_pass1"].encode()).hexdigest(), user_type=1, city=request.POST["city"], state=request.POST["state"], zip_code=request.POST["zip_code"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], driver_lic_number=request.POST["driver_lic_number"], policy_num=request.POST["policy_num"], insurance_company_id=Insurance_company.objects.get(pk=request.POST["insurance_company_id"]))
            user.save()

            messages.success(request, "User added successfuly")
            return HttpResponseRedirect(reverse("CarRental:index"))


def addusercorporate(request):
    pass
