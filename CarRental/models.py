from django.db import models

# Create your models here.


class Corporation(models.Model):
    corp_name = models.CharField(max_length=30)
    reg_num = models.CharField(max_length=12)
    discount_rate = models.FloatField()

    def __str__(self):
        return f"{self.id}"


class Insurance_company(models.Model):
    company_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.id}"


class User(models.Model):
    user_name = models.CharField(max_length=25)
    user_password = models.CharField(max_length=32)
    user_phone = models.CharField(max_length=10, blank=True)
    user_email = models.EmailField(max_length=254, blank=True)
    user_type = models.IntegerField()  # for Individual or Corporate customer
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    driver_lic_number = models.CharField(max_length=15)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=5)


class Corporate_customer(User):
    emp_id = models.IntegerField()
    corp_id = models.ForeignKey(
        Corporation, on_delete=models.CASCADE, related_name="corporate")

    def __str__(self):
        return f"{self.id}"


class Individual_customer(User):
    policy_num = models.CharField(max_length=15)
    insurance_company_id = models.ForeignKey(
        Insurance_company, on_delete=models.CASCADE, related_name="Insurance")

    def __str__(self):
        return f"{self.id}"


class Office (models.Model):
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id}"


class Vehicle_class (models.Model):
    class_name = models.CharField(max_length=20)
    daily_rate = models.FloatField()
    over_mile_fee = models.FloatField()

    def __str__(self):
        return f"{self.id}"


class Vehicle (models.Model):
    vin = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=30)
    vehicle_year = models.IntegerField()
    plate_num = models.CharField(max_length=10)
    office_id = models.ForeignKey(
        Office, on_delete=models.CASCADE, related_name="office_vehicles")
    class_id = models.ForeignKey(
        Vehicle_class, on_delete=models.CASCADE, related_name="class_vehicles")

    def __str__(self):
        return f"{self.id}"


class Coupon (models.Model):
    coupon_num = models.CharField(max_length=15, unique=True, default='')
    discount_percentage = models.FloatField()
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.id}"


class Invoice (models.Model):
    invoice_date = models.DateField(auto_now=False, auto_now_add=False)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.id}"


class Payment(models.Model):
    method = models.CharField(max_length=30)
    payment_date = models.DateField(auto_now=False, auto_now_add=False)
    card_number = models.CharField(max_length=16)
    payment_amount = models.FloatField()
    invoice_id = models.ForeignKey(
        Invoice, blank=True, on_delete=models.CASCADE, related_name="payments")

    def __str__(self):
        return f"{self.id}"


class Rental_service(models.Model):
    pickup_date = models.DateField(auto_now=False, auto_now_add=False)
    dropoff_date = models.DateField(auto_now=False, auto_now_add=False)
    start_odometer = models.FloatField(blank=True)
    end_odometer = models.FloatField(null=True, blank=True)
    daily_limit = models.IntegerField(null=True, blank=True)
    vehicle_id = models.ForeignKey(
        Vehicle, null=True, blank=True, on_delete=models.CASCADE, related_name="vehicle_rervations")
    corporate_cust_id = models.ForeignKey(
        Corporate_customer, null=True, blank=True, on_delete=models.CASCADE, related_name="Corporate_cust_rervations")
    individual_cust_id = models.ForeignKey(
        Individual_customer, null=True, blank=True, on_delete=models.CASCADE, related_name="Individual_cust_rervations")
    coupun_num = models.ForeignKey(
        Coupon, null=True,  blank=True, on_delete=models.CASCADE, related_name="coupon_rervations")
    office_pickup = models.ForeignKey(
        Office, on_delete=models.CASCADE, related_name="Pickup_office_rervations")
    office_dropoff = models.ForeignKey(
        Office, on_delete=models.CASCADE, related_name="dropoff_office_rervations")
    rental_invoice_id = models.ForeignKey(
        Invoice, null=True, blank=True, on_delete=models.CASCADE, related_name="Invoice_rervations")

    def __str__(self):
        return f"{self.id}"
