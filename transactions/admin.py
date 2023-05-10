
from django.contrib import admin

from .models import *
# Register your models here.
from django.utils.html import format_html

from django.db import models
import uuid





class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'amount', 'recipient_account', 'date', 'status', 'current_balance')
    list_filter = ('status', )
    search_fields = ('user__email', 'user__username')
    
    def client_name(self, obj):
        return obj.user.get_full_name()
    client_name.short_description = 'Client Name'
    
    def client_email(self, obj):
        return obj.user.email
    client_email.short_description = 'Client Email'
    
    def recipient_account(self, obj):
        return obj.target
    recipient_account.short_description = 'Recipient Account'
    
    def current_balance(self, obj):
        deposits = obj.user.deposits.aggregate(models.Sum('amount'))['amount__sum'] or 0
        withdrawals = obj.user.withdrawals.aggregate(models.Sum('amount'))['amount__sum'] or 0
        balance = deposits - withdrawals
        return balance
    current_balance.short_description = 'Current Balance'
    
admin.site.register(Withdrawal, WithdrawalAdmin)


class Withdrawal_internationaAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'amount', 'recipient_account', 'date', 'status', 'current_balance')
    list_filter = ('status', )
    search_fields = ('user__email', 'user__username')
    
    def client_name(self, obj):
        return obj.user.get_full_name()
    client_name.short_description = 'Client Name'
    
    def client_email(self, obj):
        return obj.user.email
    client_email.short_description = 'Client Email'
    
    def recipient_account(self, obj):
        return obj.target
    recipient_account.short_description = 'Recipient Account'
    
    def current_balance(self, obj):
        deposits = obj.user.deposits.aggregate(models.Sum('amount'))['amount__sum'] or 0
        withdrawals = obj.user.withdrawals.aggregate(models.Sum('amount'))['amount__sum'] or 0
        balance = deposits - withdrawals
        return balance
    current_balance.short_description = 'Current Balance'
    
admin.site.register(Withdrawal_internationa, Withdrawal_internationaAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'status', 'date']
    list_filter = ['status', 'date']

    def save_model(self, request, obj, form, change):
        if change:
            original_obj = Payment.objects.get(pk=obj.pk)
            if original_obj.status != 'COMPLETE' and obj.status == 'COMPLETE':
                obj.update_balance()
            elif original_obj.status == 'COMPLETE' and obj.status != 'COMPLETE':
                obj.user.balance -= original_obj.amount
                obj.user.save()
        elif obj.status == 'COMPLETE':
            obj.update_balance()

        super().save_model(request, obj, form, change)

admin.site.register(Payment, PaymentAdmin)