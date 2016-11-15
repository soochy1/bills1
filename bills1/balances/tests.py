# -*- coding: utf-8 -*-
from django.test import TestCase
from balances.models import *
from balances.scripts import calculations
from balances.scripts import inteligo
from balances.scripts.calculations import pepole_count,update_balances,update_payment,update_all,make_archive_entry,make_entry
from balances.scripts.inteligo import get_history,get_history2
import time
from datetime import date,timedelta

class CalculationsTestCase(TestCase):
    def setUp(self):
        Agreement.objects.create(name="nasze",apartment_nr=5,num_of_pepole=2,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="koralowy",apartment_nr=2,num_of_pepole=1,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="karmelowy",apartment_nr=2,num_of_pepole=1,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="beżowy",apartment_nr=2,num_of_pepole=2,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="kawowy",apartment_nr=1,num_of_pepole=2,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="niebieski",apartment_nr=1,num_of_pepole=2,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="biały",apartment_nr=1,num_of_pepole=2,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="turkusowy",apartment_nr=4,num_of_pepole=2,rent=100,email="sebastian_d@o2.pl")
        Agreement.objects.create(name="limonka",apartment_nr=3,num_of_pepole=2,rent=100,email="sebastian_d@o2.pl")

        CounterStatus.objects.create(date= (date.today() - timedelta(1)))
        CounterStatus.objects.create(date= date.today(),gas1=100,gas2=100,gas3=200,
                                        electricity1=100,
                                        electricity2=300,
                                        electricity22=300,
                                        electricity3=100,
                                        electricity4=100,
                                        electricity5=100,
                                        water1=10,
                                        water2=10,
                                        water3=10,
                                        water4=10,
                                        water5=10,
                                        water_garden=10,
                                        waterh3=10,
                                        waterh4=10,
                                        waterh5=10,
                                        electricity_adm=100)

        AgreementBalance.objects.create(name=Agreement.objects.get(name='nasze'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='koralowy'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='karmelowy'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='beżowy'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='kawowy'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='niebieski'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='biały'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='turkusowy'))
        AgreementBalance.objects.create(name=Agreement.objects.get(name='limonka'))

        Bills_prices.objects.create(date= date.today(),                                      
                                    cold_water=10,
                                    hot_water=(20),
                                    gas_unit=1,
                                    gas_abon=30,
                                    electricity_unit=0.50,
                                    electricity_abon=40,
                                    internet=20,
                                    trashes = 5)

        Account_details.objects.create(QA='bsk',login='xxxx',passwd='xxxx',
                                    account_rent='50102055581111190044700027',
                                    account_bills='51102055580000810231377320')

        Payment.objects.create(name=Agreement.objects.get(name='limonka'), amount = 200,date = "date")
        Payment_bills.objects.create(name=Agreement.objects.get(name='limonka'), amount = 200,date = "date")
        Payment.objects.create(name=Agreement.objects.get(name='limonka'), amount = 2,date = "date")
        Payment_bills.objects.create(name=Agreement.objects.get(name='limonka'), amount = 2,date = "date")

        #AgreementBalance_archive.objects.create(name=Agreement.objects.get(name='limonka'),date=date.today())



    def test_pepole_count(self):
        self.assertEqual(pepole_count()[0].number_of_pepole, 6)
        self.assertEqual(pepole_count()[1].number_of_pepole, 4)
        self.assertEqual(pepole_count()[2].number_of_pepole, 2)
        self.assertEqual(pepole_count()[3].number_of_pepole, 2)
        self.assertEqual(pepole_count()[4].number_of_pepole, 2)
        self.assertEqual(len(pepole_count()), 5)


    def test_update_balances(self):
        update_balances(pepole_count())
        self.assertEqual(AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka')).water , 300)
        self.assertEqual(round(AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka')).gas,1) , 14.6)
        self.assertEqual(AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka')).electricity , 58)
        self.assertEqual(AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka')).internet , 20)
        self.assertEqual(AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka')).trashes , 10)
        self.assertEqual(round(AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka')).total,2) , 452.71)

    """
    def test_get_history(self):
        
        history,user=get_history()
        history2=get_history2()
        self.assertEqual(user,'SEBASTIAN TOMASZ DĄBROWSKI' )
    """

        
        
    

    
    def test_update_payment(self):
        
        history=[['Data księgowania', 'Kwota', 'Nazwa nadawcy/odbiorcy', 'Opis transakcji'], ['2016-06-01', '+770.00', 'KONRAD P GIEC UL. WYSZYŃSKIEGO 7BL. 18 M.522 05-220 ZIELONKA', 'Tytuł: Pokój Kawowy - czynsz za wynajem po koju w czerwcu 2016']]

        history2=[['Data księgowania', 'Kwota', 'Nazwa nadawcy/odbiorcy', 'Opis transakcji'], ['2016-06-02', '+175.00', 'Klaudia Ćwiek  WRÓBLEWO 22/6, WRÓBLEWO 06-420 GOŁYMIN', 'Tytuł: Turkusowy Raj; opłata za media; maj']]

        user='seba'

        update_payment(history,history2)
        test_result=Payment.objects.all()[2]
        test_result2=Payment_bills.objects.all()[2]

        wzor=Payment(name=Agreement.objects.get(name='kawowy'),amount=770.00,date='2016-06-01')
        wzor2=Payment_bills(name=Agreement.objects.get(name='turkusowy'),amount=175.00,date='2016-06-02')
        self.assertEqual(test_result.name , wzor.name)
        self.assertEqual(test_result.amount , wzor.amount)
        self.assertEqual(test_result.date , wzor.date)


        self.assertEqual(test_result2.name , wzor2.name)
        self.assertEqual(test_result2.amount , wzor2.amount)
        self.assertEqual(test_result2.date , wzor2.date)
 
    
    
    def test_update_all(self):
        """
        checks result of UPDATE ALL based on predefined test values
        error in calculations gone wrong
        """
        update_all()
        result=AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka'))
        result2=AgreementBalance.objects.get(name=Agreement.objects.get(name='limonka'))
        self.assertEqual(result.prev_month_payment,102.00)
        self.assertEqual(result2.balance,202.00)

    
    def test_make_archive_entry(self):
        """
        checks type of instances returned by MAKE ARCHIVE ENTRY and MAKE ENTRY functions
        error if returned none or bad data
        """
        make_archive_entry()
        result=AgreementBalance_archive.objects.all()
        for i in range(len(result)):
            self.assertTrue(isinstance(result[i],AgreementBalance_archive))

        result2 =make_entry()
        self.assertTrue(isinstance(result2[str(date.today())][0],AgreementBalance_archive))


    
