from django.contrib import admin

from core.apps.finances.models import Cash


@admin.register(Cash)
class Cash(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        'comment',
        'created_at',
    )

    list_display_links = ('id',)
