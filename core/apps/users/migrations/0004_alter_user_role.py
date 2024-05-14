# Generated by Django 5.0.6 on 2024-05-14 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_telegram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Customer', 'Клиент'), ('Cashier', 'Кассир'), ('Moderator', 'Модератор'), ('Admin', 'Администратор')], default='Customer', max_length=50, verbose_name='Роль'),
        ),
    ]
