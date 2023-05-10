from django.contrib import admin

from .models import User, AccountDetails, UserAddress



class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','full_name' , 'contact_no', 'balance', 'account_status')

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Client Name'

    def account_status(self, obj):
        if obj.account:
            return 'Active'
        return 'Inactive'
    account_status.short_description = 'Account Status'


admin.site.register(User, UserAdmin)


@admin.register(AccountDetails)
class AccountDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'username', 'account_no', 'balance', 'total_profit', 'bonus', 'referral_bonus', 'total_deposit', 'total_withdrawal']
    search_fields = ['user__username', 'account_no']

    def full_name(self, obj):
        return obj.user.get_full_name()

    def username(self, obj):
        return obj.user.username

    full_name.short_description = 'Full Name'
    username.short_description = 'Username'


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'postal_code', 'country']
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Full Name'
    
    def country_name(self, obj):
        return dict(UserAddressForm.COUNTRY_CHOICES).get(obj.country)
    country_name.short_description = 'Country'
    
    # override the formfield_for_foreignkey method to show the full country name in the dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            kwargs["choices"] = UserAddressForm.COUNTRY_CHOICES
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(UserAddress, UserAddressAdmin)