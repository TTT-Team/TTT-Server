from django.contrib import admin

from .models import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ['bank_account_from', 'bank_account_to', 'amount', 'currency', 'method', 'date_created']
    readonly_fields = ['bank_account_from', 'bank_account_to', 'amount', 'currency', 'method', 'date_created']

    list_display = ['bank_account_from', 'bank_account_to', 'method', 'amount', 'date_created']
    list_display_links = ['date_created']
    # ordering = ['user', 'type', 'currency']
    # list_filter = ['user', 'type', 'currency']
