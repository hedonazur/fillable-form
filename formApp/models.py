# test/models.py
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4


class Book(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	publication_year = models.PositiveIntegerField()

	def __str__(self):
		return self.title


class Client(models.Model):

    PROVINCES = [
    ('Gauteng', 'Gauteng'),
    ('Free State', 'Free State'),
    ('Limpopo', 'Limpopo'),
    ]

    #Basic Fields
    clientFirstName = models.CharField(null=True, blank=True, max_length=200)
    clientLastName = models.CharField(null=True, blank=True, max_length=200)
    addressLine1 = models.CharField(null=True, blank=True, max_length=200)
    clientLogo  = models.ImageField(default='default_logo.jpg', upload_to='company_logos')
    province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    postalCode = models.CharField(null=True, blank=True, max_length=10)
    phoneNumber = models.CharField(null=True, blank=True, max_length=100)
    emailAddress = models.CharField(null=True, blank=True, max_length=100)


    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100, help_text='Not to fill')
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True, help_text='Not to fill')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Not to fill')
    last_updated = models.DateTimeField(blank=True, null=True, help_text='Not to fill')


    def __str__(self):
        return '{} {} {}'.format(self.clientFirstName, self.clientLastName, self.uniqueId)


    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.clientFirstName, self.clientLastName, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.clientFirstName, self.clientLastName, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Client, self).save(*args, **kwargs)


class Product(models.Model):
    CURRENCY = [
    ('S/', 'Sol'),
    ('$', 'USD'),
    ]

    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    currency = models.CharField(choices=CURRENCY, default='$', max_length=100)
    
    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100, help_text='Not to fill')
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True, help_text='Not to fill')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Not to fill')
    last_updated = models.DateTimeField(blank=True, null=True, help_text='Not to fill')


    def __str__(self):
        return '{} {}'.format(self.title, self.uniqueId)


    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.title, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Product, self).save(*args, **kwargs) 


class Proforma(models.Model):
     
    title = models.CharField(null=True, blank=True, max_length=100)
    salesmanName =  models.CharField(null=True, blank=True, max_length=200)
    number = models.CharField(null=True, blank=True, max_length=100)
    delivery = models.BooleanField(default=False)
    deliveryPrice = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    grandTotal = models.FloatField(null=True, blank=True, help_text='including delivery')

    #RELATED fields
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)

	#Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100, help_text='Not to fill')
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True, help_text='Not to fill')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Not to fill')
    last_updated = models.DateTimeField(blank=True, null=True, help_text='Not to fill')


    def __str__(self):
        return '{} {}'.format(self.title, self.uniqueId)


    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify()

        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Proforma, self).save(*args, **kwargs)

class Settings(models.Model):

    PROVINCES = [
    ('Gauteng', 'Gauteng'),
    ('Free State', 'Free State'),
    ('Limpopo', 'Limpopo'),
    ]

    #Basic Fields
    clientFirstName = models.CharField(null=True, blank=True, max_length=200)
    clientLastName = models.CharField(null=True, blank=True, max_length=200)
    addressLine1 = models.CharField(null=True, blank=True, max_length=200)
    clientLogo  = models.ImageField(default='default_logo.jpg', upload_to='company_logos')
    province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    postalCode = models.CharField(null=True, blank=True, max_length=10)
    phoneNumber = models.CharField(null=True, blank=True, max_length=100)
    emailAddress = models.CharField(null=True, blank=True, max_length=100)


    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100, help_text='Not to fill')
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True, help_text='Not to fill')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Not to fill')
    last_updated = models.DateTimeField(blank=True, null=True, help_text='Not to fill')


    def __str__(self):
        return '{} {} {}'.format(self.clientFirstName, self.clientLastName, self.uniqueId)


    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.clientFirstName, self.clientLastName, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.clientFirstName, self.clientLastName, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Settings, self).save(*args, **kwargs)