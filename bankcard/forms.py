from django import forms
from .models import *

class CardRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        card_request = super().save(commit=False)
        card_request.user = self.user
        if commit:
            card_request.save()
        return card_request

    class Meta:
        model = CardRequest
        fields = ['card_type']
        widgets = {
            'card_type': forms.Select(attrs={'class': 'form-control'}),
        }

# forms.py

class CardDetailsForm(forms.ModelForm):
    class Meta:
        model = CardDetails
        fields = ['card_type', 'card_number', 'expiry_date', 'cvv']
        widgets = {
            'card_type': forms.Select(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
        }

