# Generated by Django 5.0.6 on 2024-05-31 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_rename_client_transaction_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='customer_balance',
        ),
    ]