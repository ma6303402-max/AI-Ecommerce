from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'shipping_address', 'city', 'postal_code', 'country']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'john@example.com'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': '123 Main St, Apt 4B'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'New York'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10001'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'United States'}),
        }
