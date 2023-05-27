from django import forms

from .models import Diposit, Withdrawal

from .models import LoanRequest

from django import forms
from .models import LoanRequest
from .models import *

"""class CardRequestForm(forms.ModelForm):
    class Meta:
        model = CardRequest
        fields = ['card_type']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CardRequestForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user"""
class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['reason', 'amount']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }



class DepositForm(forms.ModelForm):
    class Meta:
        model = Diposit
        fields = ["amount"]


class WithdrawalForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, required=True)
    target_account_number = forms.CharField(max_length=20, required=True)
    target_bank_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Withdrawal
        fields = ["amount", "target_account_number", "target_bank_name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.user.account.balance < amount:
            raise forms.ValidationError(
                'You cannot withdraw more than your available balance.'
            )

        return amount

    def clean_target_account_number(self):
        target_account_number = self.cleaned_data['target_account_number'].strip()
        return target_account_number

    def clean_target_bank_name(self):
        target_bank_name = self.cleaned_data['target_bank_name'].strip()
        return target_bank_name



class WithdrawalInternationalForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, required=True)
    target_account_number = forms.CharField(max_length=20, required=True)
    target_bank_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Withdrawal_internationa
        fields = ["amount", "target_account_number", "target_bank_name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalInternationalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.user.account.balance < amount:
            raise forms.ValidationError(
                'You cannot withdraw more than your available balance.'
            )

        return amount

    def clean_target_account_number(self):
        target_account_number = self.cleaned_data['target_account_number'].strip()
        return target_account_number

    def clean_target_bank_name(self):
        target_bank_name = self.cleaned_data['target_bank_name'].strip()
        return target_bank_name



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'proof_of_pay']


class Client_USDTerc20Form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField()



class Client_Trc20_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()

class Client_Bitcoin_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()


class Client_Ethereum_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()
