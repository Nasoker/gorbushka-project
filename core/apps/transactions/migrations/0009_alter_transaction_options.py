# Generated by Django 5.0.6 on 2024-06-27 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_alter_transaction_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created_at'], 'verbose_name': 'Транзакция', 'verbose_name_plural': 'Транзакции'},
        ),
    ]