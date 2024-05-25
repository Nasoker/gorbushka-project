from django.contrib import admin

from .models import (
    Transaction,
    TransactionType,
)


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
    fieldsets = (
        ('Общая информация', {'fields': ('transaction_type', 'amount', 'comment')}),
        ('Данные о клиенте', {'fields': ('customer',)}),
        ('Данные о поставщике', {'fields': ('provider',)}),
        ('Системные данные', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
        ('Общая информация', {'fields': ('transaction_type', 'amount', 'comment')}),
        ('Данные о клиенте', {'fields': ('customer',)}),
        ('Данные о поставщике', {'fields': ('provider',)}),
    )

    readonly_fields = ('customer_balance', 'created_at', 'updated_at')

    list_display = (
        'id',
        'transaction_type',
        'amount',
        'comment',
        'customer',
        'customer_balance',
        'provider',
        'created_at',
        'updated_at',
    )

    list_display_links = ('transaction_type',)
