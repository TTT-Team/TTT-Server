from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Currency)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    fields = ['user', 'account_number', 'type', 'currency', 'balance']
    readonly_fields = ['user', 'account_number', 'type', 'currency', 'balance']

    list_display = ['user', 'account_number', 'type', 'currency']
    list_display_links = ['account_number']
    ordering = ['user', 'type', 'currency']
    list_filter = ['user', 'type', 'currency']



