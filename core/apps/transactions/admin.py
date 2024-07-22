from django.contrib import admin
from django.db.models import Sum

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
    change_list_template = 'admin/transactions/transaction/change_list.html'

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

    readonly_fields = ('created_at', 'updated_at')

    list_display = (
        'id',
        'transaction_type',
        'colored_amount',
        'comment',
        'customer',
        'provider',
        'created_at',
        'updated_at',
    )

    list_display_links = ('transaction_type',)

    def get_amount_sum(self):
        return Transaction.objects.aggregate(amount_sum=Sum('amount'))['amount_sum']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['amount_sum'] = self.get_amount_sum()
        return super().changelist_view(request, extra_context)
