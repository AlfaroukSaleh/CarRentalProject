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
