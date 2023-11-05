from .models import CustomUser
from .models import Order
from django import forms
from django.contrib.auth.forms import UserCreationForm


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'postal_code', 'city']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'phone_number', 'email',
                                                 'address', 'postal_code', 'city')
