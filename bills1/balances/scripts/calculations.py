#-*- coding: utf-8 -*-
from django.db import models
from balances import models
from balances.scripts import inteligo
from balances.models import Agreement,Payment,Payment_bills,AgreementBalance,AgreementBalance_archive,CounterStatus,Bills_prices
from balances.scripts.inteligo import get_history,get_history2
import re
import random
import time
import datetime
from datetime import date

class Apartment(object):
    """
    class created only to count pepole in apartments and keep this data for other calculations
    """
    def __init__(self,number):
        self.number=number
        self.number_of_pepole =0







def pepole_count():
    """
    counts number of pepole in five apartments and return list of objects of Apartment class with number of apartment and number of pepole
    """
    agreements=Agreement.objects.all()

    apartments=[]
    apartments=[Apartment(number=i) for i in range(1,6)]

    for agreement in agreements:
        if agreement.apartment_nr == 1:
            apartments[0].number_of_pepole+=agreement.num_of_pepole
        elif agreement.apartment_nr == 2:
            apartments[1].number_of_pepole+=agreement.num_of_pepole
        elif agreement.apartment_nr == 3:
            apartments[2].number_of_pepole+=agreement.num_of_pepole
        elif agreement.apartment_nr == 4:
            apartments[3].number_of_pepole+=agreement.num_of_pepole
        elif agreement.apartment_nr == 5:
            apartments[4].number_of_pepole+=agreement.num_of_pepole
        else:
            pass

    return (apartments)
           


def update_balances(apartments):
    """
    apartments= list of objects Apartment class returned by pepole_count()
    calculates AgreementBalance for each Agreement (foreign key NAME) and saves AgreementBalance in DB
    """
    prices=Bills_prices.objects.all()[0]
    

    counter_statuses = CounterStatus.objects.all()
    list_of_cs=[]
    for cs in counter_statuses:
        list_of_cs.append(cs)
    quantity_of_cs=len(list_of_cs)
    new_cs = list_of_cs[quantity_of_cs-1]
    prev_cs = list_of_cs[quantity_of_cs-2]

    gas1_wear=new_cs.gas1-prev_cs.gas1
    gas2_wear=new_cs.gas2-prev_cs.gas2
    gas3_wear=new_cs.gas3-prev_cs.gas3
    electricity1_wear=new_cs.electricity1-prev_cs.electricity1
    electricity2_wear=new_cs.electricity2-prev_cs.electricity2
    electricity22_wear=new_cs.electricity22-prev_cs.electricity22
    electricity3_wear=new_cs.electricity3-prev_cs.electricity3
    electricity4_wear=new_cs.electricity4-prev_cs.electricity4
    electricity5_wear=new_cs.electricity5-prev_cs.electricity5
    water1_wear=new_cs.water1-prev_cs.water1
    water2_wear=new_cs.water2-prev_cs.water2
    water3_wear=new_cs.water3-prev_cs.water3
    water4_wear=new_cs.water4-prev_cs.water4
    water5_wear=new_cs.water5-prev_cs.water5
    water_garden_wear=new_cs.water_garden-prev_cs.water_garden
    waterh3_wear=new_cs.waterh3-prev_cs.waterh3
    waterh4_wear=new_cs.waterh4-prev_cs.waterh4
    waterh5_wear=new_cs.waterh5-prev_cs.waterh5
    electricity2total=(electricity2_wear+electricity22_wear)
    gas3_weartotal=float(gas3_wear)-((waterh3_wear+waterh4_wear+waterh5_wear)*5.9)
    electricityadm_wear=(((float(new_cs.electricity_adm-prev_cs.electricity_adm)*prices.electricity_unit)+(prices.electricity_abon/prices.electricity_abon)/9))

    agreements = Agreement.objects.all()
    

    for agreement in agreements:
        agreement_balance= AgreementBalance.objects.get(name=agreement.id)
        if agreement.apartment_nr==1:

            agreement_balance.water=((water1_wear*prices.cold_water)/apartments[0].number_of_pepole)*agreement.num_of_pepole
            agreement_balance.gas=(((gas1_wear*prices.gas_unit)+prices.gas_abon)/apartments[0].number_of_pepole)*agreement.num_of_pepole
            agreement_balance.electricity=(((electricity1_wear*prices.electricity_unit)+prices.electricity_abon)/apartments[0].number_of_pepole)*agreement.num_of_pepole
            agreement_balance.internet=prices.internet
            agreement_balance.trashes=prices.trashes*agreement.num_of_pepole
            agreement_balance.total=agreement_balance.water\
                                    +agreement_balance.gas\
                                    +agreement_balance.electricity\
                                    +agreement_balance.internet\
                                    +agreement_balance.trashes\
                                    +electricityadm_wear
            agreement_balance.save()

        elif agreement.apartment_nr==2:

            agreement_balance.water=((water2_wear*prices.cold_water)/apartments[1].number_of_pepole)*agreement.num_of_pepole
            agreement_balance.gas=(((gas2_wear*prices.gas_unit)+prices.gas_abon)/apartments[1].number_of_pepole)*agreement.num_of_pepole
            agreement_balance.electricity=(((electricity2total*prices.electricity_unit)+prices.electricity_abon)/apartments[1].number_of_pepole)*agreement.num_of_pepole
            agreement_balance.internet=prices.internet
            agreement_balance.trashes=prices.trashes*agreement.num_of_pepole
            agreement_balance.total=agreement_balance.water\
                                    +agreement_balance.gas\
                                    +agreement_balance.electricity\
                                    +agreement_balance.internet\
                                    +agreement_balance.trashes\
                                    +electricityadm_wear
            agreement_balance.save()

        elif agreement.apartment_nr==3:

            agreement_balance.water=(((water3_wear*prices.cold_water)+(waterh3_wear*prices.hot_water)))
            agreement_balance.gas=((((gas3_weartotal*0.2)*prices.gas_unit)+(prices.gas_abon/3)))
            agreement_balance.electricity=(((electricity3_wear*prices.electricity_unit)+(prices.electricity_abon/5)))
            agreement_balance.internet=prices.internet
            agreement_balance.trashes=prices.trashes*agreement.num_of_pepole
            agreement_balance.total= agreement_balance.water\
                                     +agreement_balance.gas\
                                     +agreement_balance.electricity\
                                     +agreement_balance.internet\
                                     +agreement_balance.trashes\
                                     +electricityadm_wear
            agreement_balance.save()
            #
        elif agreement.apartment_nr==4:

            agreement_balance.water=((((water4_wear*prices.cold_water))+((waterh4_wear*prices.hot_water))))
            agreement_balance.gas=((((gas3_weartotal*0.3)*prices.gas_unit)+(prices.gas_abon/3)))
            agreement_balance.electricity=(((electricity4_wear*prices.electricity_unit)+(prices.electricity_abon/5)))
            agreement_balance.internet=prices.internet
            agreement_balance.trashes=prices.trashes*agreement.num_of_pepole
            agreement_balance.total=agreement_balance.water\
                                    +agreement_balance.gas\
                                    +agreement_balance.electricity\
                                    +agreement_balance.internet\
                                    +agreement_balance.trashes\
                                    +electricityadm_wear
            agreement_balance.save()
            #
        elif agreement.apartment_nr==5:

            agreement_balance.water=(((water5_wear*prices.cold_water))+(waterh5_wear*prices.hot_water))
            agreement_balance.gas=(((gas3_weartotal*0.5)*prices.gas_unit)+(prices.gas_abon/3))
            agreement_balance.electricity=((electricity5_wear*prices.electricity_unit)+(prices.electricity_abon/5))
            agreement_balance.internet=0
            agreement_balance.total=agreement_balance.water\
                                    +agreement_balance.gas\
                                    +agreement_balance.electricity\
                                    +electricityadm_wear\
                                    +water_garden_wear*5
            agreement_balance.save()
        else:
            pass
    return True

def update_payment(history,history2):

    """
    history and history2 should be lists returned by get_history() from inteligo.py module
    checks lists history and history2 if there was proper payment and saves it into payments and payments_bills
    """

    agreements= Agreement.objects.all()

    for agreement in agreements:

        pattern = re.compile(agreement.name,re.I)

        for row in history:
            result = pattern.search(row[3])
            if (result != None):
                if float(row[1])> 0:
                    payment = Payment.objects.create(name = agreement, amount = float(row[1]),date = row[0])
                    payment.save()


    for agreement in agreements:

            pattern = re.compile(agreement.name,re.I)

            for row in history2:
                result = pattern.search(row[3])
                if (result != None):
                    if float(row[1])> 0:
                        payment_b = Payment_bills.objects.create(name = agreement, amount = float(row[1]),date = row[0])
                        payment_b.save()

def update_all():

    #update_balances(pepole_count())
    """
    updates AgreementBalances fields that depends on payments
    updated fields should be prev_month_payment and balance
    """
    
    balances = AgreementBalance.objects.all()

    for balance in balances:
        amount = 0
        try:
            payments = Payment.objects.filter(name=balance.name)
            for payment in payments:
                amount +=  payment.amount
                payment.delete()
        except:
            pass

        amount2 = 0 
        try:
            payments2 = Payment_bills.objects.filter(name=balance.name)
            for  payment in payments2:
                amount2 +=  payment.amount
                payment.delete()
        except:
            pass

        agreement=Agreement.objects.get(name=str(balance.name))
        balance.prev_month_payment = amount-agreement.rent
        balance.balance += (amount2-balance.total)
        balance.save()



def make_archive_entry():
    """
    generates objects of AgreementBalance_archive based on actual state of actual objects of AgreementBalance
    and adds date of this operation which is date of "snapshot" of objects 
    """
    agreements = Agreement.objects.all()

    for agreement in agreements:
            balance=AgreementBalance.objects.get(name=agreement)
            new_archive_balance=AgreementBalance_archive.objects.create(name=agreement,date=date.today())
            new_archive_balance.name=balance.name
            new_archive_balance.water=balance.water
            new_archive_balance.gas=balance.gas
            new_archive_balance.electricity=balance.electricity
            new_archive_balance.internet=balance.internet
            new_archive_balance.total=balance.total
            new_archive_balance.trashes=balance.trashes
            new_archive_balance.prev_month_payment=balance.prev_month_payment
            new_archive_balance.balance=balance.balance
            new_archive_balance.save()
            

def make_entry():
    """
    generates a dictionary like {'date':[AgreementBalance_archiveOBJECT1,AgreementBalance_archiveOBJECT2]}
    and returns it
    """

    archive_balances = AgreementBalance_archive.objects.all()
    balances_list=[]
    for balance in archive_balances:
        balances_list.append(balance)

    date = balances_list[0].date
    dates=[]
    dates.append(str(date))
    entry=[]
    entry.append([])
    i=0

    for balance in balances_list:

        if balance.date == date:
            entry[i].append(balance)

        else:
            date=balance.date
            entry.append([])
            i+=1
            entry[i].append(balance)

            dates.append(str(date))

    entry2={}
    i=0
    for date in dates:
        entry2[date]=entry[i]
        i+=1

    return (entry2)
