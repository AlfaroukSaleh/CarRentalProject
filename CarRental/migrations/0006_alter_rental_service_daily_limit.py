# Generated by Django 4.0.4 on 2022-05-01 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarRental', '0005_alter_rental_service_corporate_cust_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental_service',
            name='daily_limit',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
