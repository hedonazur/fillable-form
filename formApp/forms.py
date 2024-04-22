from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json

#Form Layout from Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


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
                required=False, 
                widget=forms.TextInput(
                    attrs={'class': 'form-control'}))
    salesmanName = forms.CharField(
                required=True, 
                widget=forms.TextInput(
                    attrs={'class': 'form-control'}))
    delivery = forms.BooleanField(
                required=False, 
                widget=forms.CheckboxInput(
                    attrs={'class': 'form-check-input'}))
    deliveryPrice = forms.FloatField(
                required=False, 
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'}))
    total = forms.FloatField(
                required=False, 
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'}))
    grandTotal = forms.FloatField(
                required=False, 
                widget=forms.NumberInput(
                    attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6'),
                Column('salesmanName', css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column('delivery', css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column('deliveryPrice', css_class='form-group col-md-6'),
                Column('total', css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column('grandTotal', css_class='form-group col-md-6'),
                css_class='form-row'),

            Submit('submit', ' EDIT PROFORMA '))

    class Meta:
        model = Proforma
        fields = ['title', 'salesmanName', 'delivery', 'deliveryPrice', 'total', 'grandTotal']




class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['clientFirstName', 'clientLastName', 'clientLogo', 'addressLine1', 'province', 'postalCode', 'phoneNumber', 'emailAddress']


class ClientSelectForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.initial_client = kwargs.pop('initial_client')
        self.CLIENT_LIST = Client.objects.all()
        self.CLIENT_CHOICES = [('-----', '--Select a Client--')]


        for client in self.CLIENT_LIST:
            d_t = (client.uniqueId, client.clientFirstName)
            self.CLIENT_CHOICES.append(d_t)


        super(ClientSelectForm,self).__init__(*args,**kwargs)

        self.fields['client'] = forms.ChoiceField(
                                        label='Choose a related client',
                                        choices = self.CLIENT_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control mb-3'}),)

    class Meta:
        model = Proforma
        fields = ['client']


    def clean_client(self):
        c_client = self.cleaned_data['client']
        if c_client == '-----':
            return self.initial_client
        else:
            return Client.objects.get(uniqueId=c_client)
















# <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
# <input type="password" class="form-control" id="floatingPassword" placeholder="Password">