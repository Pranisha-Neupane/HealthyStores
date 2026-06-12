"""Checkout form — pre-filled from the user's profile where possible."""
from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '98XXXXXXXX'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                             'placeholder': 'Street, City, Landmark'}),
            'payment_method': forms.RadioSelect(),
        }
