from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

import hashlib
from itertools import chain
from .models import Individual_customer, Corporate_customer, Insurance_company, Corporation, Rental_service, Office, Vehicle, Vehicle_class, Payment, Invoice, Coupon
from django.contrib.auth import authenticate, login, logout
import datetime

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("CarRental:login"))
    else:
        return render(request, "CarRental/index.html", {
            "Car_classes": Vehicle_class.objects.all(),
            "Offices": Office.objects.all()
        })


def adduserindividual(request):  # used for adding Indivdual users
    if request.method == "GET":
        return render(request, "CarRental/adduserindividual.html", {
            "Insurance_companies": Insurance_company.objects.all(),
            "FormItem": [('user_name', 'text', 'Username'),
                         ('user_email', 'email', 'Email'),
                         ('user_phone', 'tel', 'Phone Number'),
                         ('user_pass1', 'passward', 'Password'),
                         ('user_pass2', 'passward', 'Comfirm Password'),
                         ('first_name', 'text', 'First Name'),
                         ('last_name', 'text', 'Last Name'),
                         ('city', 'text', 'City'),
                         ('state', 'text', 'State'),
                         ('zip_code', 'number', 'ZipCode'),
                         ('driver_lic_number', 'text', 'Lisence Number'),
                         ('policy_num', 'text', 'Ins. Policy Number')
                         ]
        })

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
                return HttpResponseRedirect(reverse("CarRental:adduserindividual"))

                # Checks if this number was previously used
            user_phone_validator = Individual_customer.objects.filter(
                user_phone=request.POST["user_phone"]).first()

            if user_phone_validator is not None:
                messages.error(
                    request, "This phone number was previously used!")
                return HttpResponseRedirect(reverse("CarRental:adduserindividual"))

            if request.POST["user_pass1"] != request.POST["user_pass2"]:
                messages.error(
                    request, "The two passwords don't match!")
                return HttpResponseRedirect(reverse("CarRental:adduserindividual"))

                # Creates a new user
            user = Individual_customer(user_name=request.POST["user_name"], user_email=request.POST["user_email"], user_phone=request.POST[
                "user_phone"], user_password=hashlib.md5(request.POST["user_pass1"].encode()).hexdigest(), user_type=1, city=request.POST["city"], state=request.POST["state"], zip_code=request.POST["zip_code"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], driver_lic_number=request.POST["driver_lic_number"], policy_num=request.POST["policy_num"], insurance_company_id=Insurance_company.objects.get(pk=request.POST["insurance_company_id"]))
            user.save()
            user2 = User.objects.create_user(username=request.POST["user_name"],
                                             email=request.POST["user_email"],
                                             password=request.POST["user_pass1"])
            u = authenticate(
                request, username=request.POST["user_name"], password=request.POST["user_pass1"])
            messages.success(request, "User added successfuly")
            login(request, u)
            messages.success(request, "User added successfuly")
            return HttpResponseRedirect(reverse("CarRental:index"))


def addusercorporate(request):  # used for adding Corporate users
    if request.method == "GET":
        return render(request, "CarRental/addusercorporate.html", {
            "Corporations": Corporation.objects.all(),
            "FormItem": [('user_name', 'text', 'Username'),
                         ('user_email', 'email', 'Email'),
                         ('user_phone', 'tel', 'Phone Number'),
                         ('user_pass1', 'passward', 'Password'),
                         ('user_pass2', 'passward', 'Comfirm Password'),
                         ('first_name', 'text', 'First Name'),
                         ('last_name', 'text', 'Last Name'),
                         ('city', 'text', 'City'),
                         ('state', 'text', 'State'),
                         ('zip_code', 'number', 'ZipCode'),
                         ('driver_lic_number', 'text', 'Lisence Number'),
                         ('emp_id', 'number', 'Employee ID')
                         ]
        })

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
                return HttpResponseRedirect(reverse("CarRental:addusercorporate"))

                # Checks if this number was previously used
            user_phone_validator = Individual_customer.objects.filter(
                user_phone=request.POST["user_phone"]).first()

            if user_phone_validator is not None:
                messages.error(
                    request, "This phone number was previously used!")
                return HttpResponseRedirect(reverse("CarRental:addusercorporate"))

            if request.POST["user_pass1"] != request.POST["user_pass2"]:
                messages.error(
                    request, "The two passwords don't match!")
                return HttpResponseRedirect(reverse("CarRental:addusercorporate"))

                # Creates a new user
            user = Corporate_customer(user_name=request.POST["user_name"], user_email=request.POST["user_email"], user_phone=request.POST[
                "user_phone"], user_password=hashlib.md5(request.POST["user_pass1"].encode()).hexdigest(), user_type=1, city=request.POST["city"], state=request.POST["state"], zip_code=request.POST["zip_code"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], driver_lic_number=request.POST["driver_lic_number"], emp_id=request.POST["emp_id"], corp_id=Corporation.objects.get(pk=request.POST["corp_id"]))
            user.save()
            user2 = User.objects.create_user(username=request.POST["user_name"],
                                             email=request.POST["user_email"],
                                             password=request.POST["user_pass1"])
            u = authenticate(
                request, username=request.POST["user_name"], password=request.POST["user_pass1"])
            messages.success(request, "User added successfuly")
            login(request, u)
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
                    pk=request.POST["pickup_office_id"]), office_dropoff=Office.objects.get(pk=request.POST["dropoff_office_id"]), individual_cust_id=individual_customer, vehicle_class=Vehicle_class.objects.get(pk=request.POST["vehicle_class_id"]))
                reservation.save()
                # Head to the payment page with the reservation ID
                return HttpResponseRedirect(reverse("CarRental:payment", args=(reservation.id,)))
            else:
                # This means a corporate customer is making a reservation
                reservation = Rental_service(pickup_date=request.POST["pickup_date"], dropoff_date=request.POST["dropoff_date"], office_pickup=Office.objects.get(
                    pk=request.POST["pickup_office_id"]), office_dropoff=Office.objects.get(pk=request.POST["dropoff_office_id"]), corporate_cust_id=corporate_customer, vehicle_class=Vehicle_class.objects.get(pk=request.POST["vehicle_class_id"]))
                reservation.save()
                # Head to the payment page with the reservation ID
                return HttpResponseRedirect(reverse("CarRental:payment", args=(reservation.id,)))
    return HttpResponseRedirect(reverse("CarRental:index"))


def payment(request, reservation_id):
    if not request.user.is_authenticated:
        messages.error(request, "You are not authorized to view this page!")
        return HttpResponseRedirect(reverse("CarRental:login"))

    else:
        if request.method == "POST":
            dropoff_date = Rental_service.objects.get(
                pk=reservation_id).dropoff_date
            pickup_date = Rental_service.objects.get(
                pk=reservation_id).pickup_date
            daily_rate = Rental_service.objects.get(
                pk=reservation_id).vehicle_class.daily_rate
            # Calculate amount without coupon
            amount = (dropoff_date - pickup_date).days * daily_rate

            # Calculate amount with coupon
            if request.POST["coupon_num"] != '':
                coupon = Coupon.objects.get(
                    coupon_num=request.POST["coupon_num"])
                if coupon.start_date <= dropoff_date and coupon.end_date >= dropoff_date:
                    amount = amount * (1 - coupon.discount_percentage / 100.)

            invoice = Invoice(
                amount=amount, invoice_date=datetime.date.today())
            invoice.save()
            payment = Payment(invoice_id=Invoice.objects.get(id=invoice.id), payment_amount=amount, payment_date=datetime.date.today(
            ), card_number=request.POST["card_number"], name_on_card=request.POST["name_on_card"], exp_date=request.POST["exp_date"], cvv=request.POST["cvv"])
            payment.save()
            return HttpResponseRedirect(reverse("CarRental:invoice", args=(payment.id,)))

    return render(request, "CarRental/payment.html", {"reservation_id": reservation_id})


def invoice(request, payment_id):
    if not request.user.is_authenticated:
        messages.error(request, "You are not authorized to view this page!")
        return HttpResponseRedirect(reverse("CarRental:login"))

    request.session["amount"] = Payment.objects.get(
        pk=payment_id).payment_amount
    request.session["payment_date"] = Payment.objects.get(
        pk=payment_id).payment_date.strftime('%m/%d/%Y')

    return render(request, "CarRental/invoice.html", {
        "amount": request.session["amount"],
        "payment_date": request.session["payment_date"]
    })
