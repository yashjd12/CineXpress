# Generated by Django 4.1.1 on 2022-11-12 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_razorpaypayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='razorpaypayment',
            old_name='payment_order_id',
            new_name='provider_order_id',
        ),
    ]