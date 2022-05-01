from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

import hashlib
from itertools import chain
from .models import Individual_customer, Corporate_customer, Insurance_company, Corporation, Rental_service, Office
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("CarRental:login"))
    else:
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
            user2 = User.objects.create_user(username=request.POST["user_name"],
                                             email=request.POST["user_email"],
                                             password=request.POST["user_pass1"])
            messages.success(request, "User added successfuly")
            return HttpResponseRedirect(reverse("CarRental:index"))


def addusercorporate(request):  # used for adding Corporate users
    if request.method == "GET":
        return render(request, "CarRental/addusercorporate.html")

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
                return HttpResponseRedirect(reverse("addusercorporate"))

                # Checks if this number was previously used
            user_phone_validator = Individual_customer.objects.filter(
                user_phone=request.POST["user_phone"]).first()

            if user_phone_validator is not None:
                messages.error(
                    request, "This phone number was previously used!")
                return HttpResponseRedirect(reverse("addusercorporate"))

            if request.POST["user_pass1"] != request.POST["user_pass2"]:
                messages.error(
                    request, "The two passwords don't match!")
                return HttpResponseRedirect(reverse("addusercorporate"))

                # Creates a new user
            user = Corporate_customer(user_name=request.POST["user_name"], user_email=request.POST["user_email"], user_phone=request.POST[
                "user_phone"], user_password=hashlib.md5(request.POST["user_pass1"].encode()).hexdigest(), user_type=1, city=request.POST["city"], state=request.POST["state"], zip_code=request.POST["zip_code"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], driver_lic_number=request.POST["driver_lic_number"], emp_id=request.POST["emp_id"], corp_id=Corporation.objects.get(pk=request.POST["corp_id"]))
            user.save()
            user2 = User.objects.create_user(username=request.POST["user_name"],
                                             email=request.POST["user_email"],
                                             password=request.POST["user_pass1"])
            messages.success(request, "User added successfuly")
            return HttpResponseRedirect(reverse("CarRental:index"))


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, "You are not authorized to view this page!")
        return HttpResponseRedirect(reverse("CarRental:index"))

    if request.method == "POST":
        # here we enter the email address of the user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("CarRental:index"))
        else:
            return render(request, "CarRental/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "CarRental/login.html")


def logout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not authorized to view this page!")
        return HttpResponseRedirect(reverse("CarRental:login"))
    else:
        logout(request)
        return render(request, "CarRental/login.html", {
            "message": "Logged out."
        })


def makereservation(request):
    if request.method == "GET":
        return render(request, "CarRental/index.html")

    if not request.user.is_authenticated:
        messages.error(request, "You are not authorized to view this page!")
        return HttpResponseRedirect(reverse("CarRental:login"))

    else:
        if request.method == "POST":
            individual_customer = Individual_customer.objects.filter(
                user_name=request.user.username).first()  # Checking if this user is an individual customer
            corporate_customer = Corporate_customer.objects.filter(
                user_name=request.user.username).first()  # checking if the user is a corporate customer

            if individual_customer is not None:
                # This means we have an individual customer making a reservation
                reservation = Rental_service(pickup_date=request.POST["pickup_date"], dropoff_date=request.POST["dropoff_date"], office_pickup=Office.objects.get(
                    pk=request.POST["pickup_office_id"]), office_dropoff=Office.objects.get(pk=request.POST["dropoff_office_id"]), individual_cust_id=individual_customer, start_odometer=request.POST["start_odometer"])
                reservation.save()
                return HttpResponseRedirect(reverse("CarRental:index"))
            else:
                # This means a corporate customer is making a reservation
                reservation = Rental_service(pickup_date=request.POST["pickup_date"], dropoff_date=request.POST["dropoff_date"], office_pickup=Office.objects.get(
                    pk=request.POST["pickup_office_id"]), office_dropoff=Office.objects.get(pk=request.POST["dropoff_office_id"]), corporate_cust_id=corporate_customer, start_odometer=request.POST["start_odometer"])
                reservation.save()
                return HttpResponseRedirect(reverse("CarRental:index"))
    return HttpResponseRedirect(reverse("CarRental:index"))
