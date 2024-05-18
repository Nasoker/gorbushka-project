# Generated by Django 5.0.6 on 2024-05-18 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Баланс'),
        ),
    ]
