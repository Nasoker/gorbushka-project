# Generated by Django 5.0.4 on 2024-04-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='provider',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Поставщик'),
        ),
    ]
