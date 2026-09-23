from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'stock', 'image_url', 'tags', 'is_featured']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Detailed description...'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input'}),
            'image_url': forms.URLInput(attrs={'class': 'form-input'}),
            'tags': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ai, smart, wireless'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
