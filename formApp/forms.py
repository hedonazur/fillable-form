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
    title = forms.CharField(
                # required=True, 
                widget=forms.TextInput(
                    attrs={'class': 'form-control'}))
    salesmanName = forms.CharField(
                # required=True, 
                widget=forms.TextInput(
                    attrs={'class': 'form-control'}))
    delivery = forms.BooleanField(
                # required=True, 
                widget=forms.CheckboxInput(
                    attrs={'class': 'form-check-input'}))
    deliveryPrice = forms.FloatField(
                # required=True, 
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'}))
    total = forms.FloatField(
                # required=True, 
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'}))
    grandTotal = forms.FloatField(
                # required=True, 
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'}))
    

    class Meta:
        model = Proforma
        fields = ['title', 'salesmanName', 'delivery', 'deliveryPrice', 'total', 'grandTotal']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['clientFirstName', 'clientLastName', 'clientLogo', 'addressLine1', 'province', 'postalCode', 'phoneNumber', 'emailAddress']


class ClientSelectForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.CLIENT_LIST = Client.objects.all()
        self.CLIENT_CHOICES = [('-----', '---Please Select---')]

        for client in self.CLIENT_LIST:
            d_t = (client.uniqueId, '{} {}'.format(client.clientFirstName, client.clientLastName))
            self.CLIENT_CHOICES.append(d_t)


        super(ClientSelectForm,self).__init__(*args,**kwargs)

        self.fields['client'] = forms.ChoiceField(
                                        label='Choose a client',
                                        choices = self.CLIENT_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control mb-3'}),)

    class Meta:
        model = Proforma
        fields = ['client']

    def clean_client(self):
        c_client = self.cleaned_data['client']
        return Client.objects.get(uniqueId=c_client)
















# <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
# <input type="password" class="form-control" id="floatingPassword" placeholder="Password">