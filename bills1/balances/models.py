from __future__ import unicode_literals

from django.db import models

# Create your models here.



from django.db import models
import time
import datetime


# Create your models here.


class Agreement(models.Model):
    name = models.CharField(max_length=20,default="None")
    apartment_nr = models.IntegerField(default=0)
    num_of_pepole= models.IntegerField(default=1)
    rent = models.IntegerField(default=0)
    email = models.CharField(max_length=50,default="None")

    def __str__(self):
        return "{name}".format(name=self.name)

class Payment(models.Model):
    amount = models.FloatField(default=0)
    name= models.ForeignKey(Agreement)
    date = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "{name}".format(name=self.name)

class Payment_bills(models.Model):
    amount = models.FloatField(default=0)
    name= models.ForeignKey(Agreement)
    date = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "{name}".format(name=self.name)

class AgreementBalance(models.Model):
    name= models.ForeignKey(Agreement)
    water = models.FloatField(max_length=20, default=0)
    gas= models.FloatField(max_length=20, default=0)
    electricity = models.FloatField(max_length=20, default=0)
    internet = models.FloatField(max_length=20, default=0)
    trashes = models.IntegerField(default = 0)
    total= models.FloatField(max_length=20, default=0)
    prev_month_payment = models.FloatField(max_length=20, default=0)
    balance = models.FloatField(max_length=20, default=0)


    def __str__(self):
        return "{name}".format(name=self.name)

class AgreementBalance_archive(models.Model):
    date = models.DateField()
    name= models.ForeignKey(Agreement)
    water = models.FloatField(max_length=20, default=0)
    gas= models.FloatField(max_length=20, default=0)
    electricity = models.FloatField(max_length=20, default=0)
    internet = models.FloatField(max_length=20, default=0)
    trashes = models.IntegerField(default = 0)
    total= models.FloatField(max_length=20, default=0)
    prev_month_payment = models.FloatField(max_length=20, default=0)
    balance = models.FloatField(max_length=20, default=0)

    def __str__(self):
        return ("{date} {name}".format(date=self.date,name=self.name))
    

class CounterStatus(models.Model):
    date = models.DateField()
    gas1=models.FloatField( default=0)
    gas2=models.FloatField( default=0)
    gas3=models.FloatField( default=0)
    electricity1=models.FloatField( default=0)
    electricity2=models.FloatField( default=0)
    electricity22=models.FloatField( default=0)
    electricity3=models.FloatField( default=0)
    electricity4=models.FloatField( default=0)
    electricity5=models.FloatField( default=0)
    water1=models.FloatField( default=0)
    water2=models.FloatField( default=0)
    water3=models.FloatField( default=0)
    water4=models.FloatField( default=0)
    water5=models.FloatField( default=0)
    water_garden=models.FloatField( default=0)
    waterh3=models.FloatField( default=0)
    waterh4=models.FloatField( default=0)
    waterh5=models.FloatField( default=0)
    electricity_adm=models.FloatField( default=0)

    def __str__(self):
        return str(self.date)

class Bills_prices(models.Model):
    date=date = models.DateField()
    cold_water = models.FloatField(default=0)
    hot_water = models.FloatField(default=0)
    gas_unit = models.FloatField(default=0)
    gas_abon = models.FloatField(default=0)
    electricity_unit = models.FloatField(default=0)
    electricity_abon = models.FloatField(default=0)
    internet = models.FloatField(default=0)
    trashes = models.FloatField(default=0)

    def __str__(self):
        return str(self.date)

class Account_details(models.Model):
    QA=models.CharField(max_length=10,default='')
    login= models.CharField(max_length=20,default='')
    passwd= models.CharField(max_length=20, default='')
    account_rent=models.CharField(max_length=30, default='')
    account_bills=models.CharField(max_length=30, default='')
    admin_email=models.CharField(max_length=30, default='')
    admin_email_login=models.CharField(max_length=30, default='')
    admin_email_password=models.CharField(max_length=30, default='')




