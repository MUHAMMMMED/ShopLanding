# Generated by Django 4.2.13 on 2024-09-12 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_remove_payment_status_payment_paid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]