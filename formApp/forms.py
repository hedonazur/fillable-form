from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json



class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientFirstName', 'clientLastName', 'clientLogo', 'addressLine1', 'province', 'postalCode', 'phoneNumber', 'emailAddress']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'quantity', 'price', 'currency']


class ProformaForm(forms.ModelForm):
    class Meta:
        model = Proforma
        fields = ['title', 'salesmanName', 'delivery', 'deliveryPrice', 'total', 'grandTotal', 'client', 'product']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['clientFirstName', 'clientLastName', 'clientLogo', 'addressLine1', 'province', 'postalCode', 'phoneNumber', 'emailAddress']






















# <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
# <input type="password" class="form-control" id="floatingPassword" placeholder="Password">