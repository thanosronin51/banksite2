from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    gift_card_type = forms.ChoiceField(choices=[('apple', 'Apple Card'), ('amazon', 'Amazon Card'), ('steam', 'Steam Card'), ('xbox', 'Xbox Card')])

    class Meta:
        model = Payment
        fields = ['amount', 'proof_of_pay', 'gift_card_type']