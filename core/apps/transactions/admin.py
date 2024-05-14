from django.contrib import admin
from .models import TransactionType, Transaction


@admin.register(TransactionType)
class TransactionType(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'created_at',
        'updated_at',
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transaction_type',
        'client',
        'client_balance',
        'provider',
        'amount',
        'comment',
        'created_at',
        'updated_at',
    )
