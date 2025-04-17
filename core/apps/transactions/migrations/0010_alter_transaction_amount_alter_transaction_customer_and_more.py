# Generated by Django 5.0.6 on 2025-04-17 19:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_alter_transaction_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Сумма операции'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='customer',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'Customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transaction_types', to='transactions.transactiontype', verbose_name='Тип транзакции'),
        ),
        migrations.CreateModel(
            name='TransactionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('provider', models.CharField(blank=True, max_length=255, null=True, verbose_name='Поставщик')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Сумма операции')),
                ('comment', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Примечание')),
                ('status', models.CharField(choices=[('requested', 'Запрошен'), ('approved', 'Подтвержден'), ('rejected', 'Отклонен')], default='requested', max_length=25, verbose_name='Статус')),
                ('approver', models.ForeignKey(blank=True, limit_choices_to={'role': 'Admin'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approvers', to=settings.AUTH_USER_MODEL, verbose_name='Подтвердил/Отклонил')),
                ('customer', models.ForeignKey(blank=True, limit_choices_to={'role': 'Customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_customers', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('requester', models.ForeignKey(blank=True, limit_choices_to={'role': ['Cashier', 'Moderator', 'Admin']}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requesters', to=settings.AUTH_USER_MODEL, verbose_name='Запросил')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='request_transaction_types', to='transactions.transactiontype', verbose_name='Тип транзакции')),
            ],
            options={
                'verbose_name': 'Запрос Транзакции',
                'verbose_name_plural': 'Запросы транзакций',
                'ordering': ['-created_at'],
            },
        ),
    ]
