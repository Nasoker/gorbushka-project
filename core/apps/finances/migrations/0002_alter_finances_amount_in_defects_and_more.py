# Generated by Django 5.0.6 on 2024-06-16 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finances',
            name='amount_in_defects',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Сумма в браке'),
        ),
        migrations.AlterField(
            model_name='finances',
            name='amount_in_goods',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Сумма в товаре'),
        ),
    ]