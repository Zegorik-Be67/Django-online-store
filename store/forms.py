from django import forms
from .models import Store

class NewProduct(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['image', 'title', 'description', 'whose', 'price']