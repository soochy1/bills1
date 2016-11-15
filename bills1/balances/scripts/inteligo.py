#-*- coding: utf-8 -*-
import codecs
import requests
from bs4 import BeautifulSoup as bs
from balances.models import Account_details
import csv
import io
import datetime


def daty():
    '''
	function generates two strings 
	date_from and date_to , this dates are neccesary for function get_history to search payments in specific peroid of time betwen those dates
	'''
    date_to = datetime.date.today()
    months_and_days={1:31,
                    2:28,
                    3:31,
                    4:30,
                    5:31,
                    6:30,
                    7:31,
                    8:31,
                    9:30,
                    10:31,
                    11:30,
                    12:31
                    }

    if date_to.day <= 15:
        date_from= date_to.replace(month=date_to.month-1,day=1)
        date_to= date_to.replace(month=date_to.month-1)
        for month in range(1,12):
            if date_to.month == month:
                date_to= date_to.replace(day=months_and_days[month])

    elif date_to.day > 15:
        date_from= date_to.replace(day=1)

    return (date_from,date_to)





def get_hidden_inputs(html_data):
    html_proc=bs(html_data,"html.parser")
    html_inputs = html_proc.findAll('input', {'type':'hidden'})
    inputs=dict()
    for elem in html_inputs:
        inputs[elem['name']]=elem.get('value', '')
    return (inputs)

def get_user_name(text):
    html = bs(text,"html.parser")
    return html.find('ul', {'class':'user-info'}).find('li').find('span').text

def get_active_menu(text):
    html = bs(text,"html.parser")
    return html.find('div', {'class':'active'}).get('title')

    """
    Function log in into inteligo acount and gets data form history of transactions and returns list with transactions

    """

def get_history():

    acd = Account_details.objects.get(QA='bsk')
    with requests.Session() as s:
        url = 'https://inteligo.pl/secure/igo2';
        r = s.get(url)
        inputs = get_hidden_inputs(r.text)
        inputs['client_id_field'] = str(acd.login)
        inputs['password_field'] = str(acd.passwd)
        #LOG IN
        r=s.post(url, data=inputs)
        rtext = r.text
        #rtext = rtext.decode('utf-8')
        user=get_user_name(rtext)
        #print("Menu:", get_active_menu(r.text))


        #go to history page
        inputs = get_hidden_inputs(r.text)
        inputs['dynsub_ex_dd85f9458761c8ce69def60370866b05d091f7f5_3'] = ''
        r = s.post(url, data=inputs)

        date_from,date_to = daty()

        #show history of selected account
        inputs = get_hidden_inputs(r.text)
        inputs['dynsub_ex_b390f775eeab31a9b23eb69013270c1751fdd32b'] = 'Pokaż'
        inputs['fields_search-selected_acc'] =str(acd.account_rent)
        
        inputs['fields_search-show_advanced'] = 1
        inputs['fields_advanced-date_range-since'] =str(date_from)
        inputs['fields_advanced-date_range-to'] =str(date_to)
        inputs['fields_advanced-date_range-select']= 'other'
        inputs['fields_advanced-filter_tx_type']='ACC:ALL'
        

        r = s.post(url, data=inputs)

        #save history in memory as csv
        inputs = get_hidden_inputs(r.text)
        inputs['fields_search-selected_acc'] =acd.account_rent
        inputs['format'] = 'csv'
        inputs['dynsub_ex_6a174157eec0e7b59a2180ba0936938d4668b42d'] = ''
        r =s.post(url, data=inputs)
        r2=codecs.decode(r.content,'Windows-1250')

        history=[]




        csvfile = csv.reader(io.StringIO(r2))



        #saves in list rows with DATA KWOTA WPLACAJACY TYTUŁ
        for row in csvfile:
            #print('row: ',row)
            history.append([row[1],row[4],row[8],row[9]])






    return (history,user)

def get_history2():

    acd = Account_details.objects.get(QA='bsk')
    with requests.Session() as s:
        url = 'https://inteligo.pl/secure/igo2';
        r = s.get(url)
        inputs = get_hidden_inputs(r.text)
        inputs['client_id_field'] = acd.login
        inputs['password_field'] = acd.passwd
        r=s.post(url, data=inputs)
        inputs = get_hidden_inputs(r.text)
        inputs['dynsub_ex_dd85f9458761c8ce69def60370866b05d091f7f5_3'] = ''
        r = s.post(url, data=inputs)
        date_from,date_to = daty()
        inputs = get_hidden_inputs(r.text)
        inputs['dynsub_ex_b390f775eeab31a9b23eb69013270c1751fdd32b'] = 'Pokaż'
        inputs['fields_search-selected_acc'] =acd.account_bills
        inputs['fields_search-show_advanced'] = 1
        inputs['fields_advanced-date_range-since'] =str(date_from)
        inputs['fields_advanced-date_range-to'] =str(date_to)
        inputs['fields_advanced-date_range-select']= 'other'
        inputs['fields_advanced-filter_tx_type']='ACC:ALL'
        r = s.post(url, data=inputs)
        inputs = get_hidden_inputs(r.text)
        inputs['fields_search-selected_acc'] =acd.account_bills
        inputs['format'] = 'csv'
        inputs['dynsub_ex_6a174157eec0e7b59a2180ba0936938d4668b42d'] = ''
        r =s.post(url, data=inputs)
        r2=codecs.decode(r.content,'Windows-1250')
        history2=[]
        csvfile = csv.reader(io.StringIO(r2))
        for row in csvfile:
            history2.append([row[1],row[4],row[8],row[9]])
    return history2
