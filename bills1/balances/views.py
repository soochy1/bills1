from django.shortcuts import render
from django.views.generic import ListView
from balances.models import Agreement,AgreementBalance,CounterStatus
from balances.forms import GetCountersData
import datetime
from datetime import date
from django.http import HttpResponseRedirect
from balances.scripts.calculations import update_payment,make_archive_entry,make_entry,pepole_count,update_balances,update_all
from balances.scripts.inteligo import get_history,get_history2
from balances.scripts.mail import send_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

# Create your views here.
@login_required
def index(request):
    return render(request, 'balances/index.html',{})


class AgreementListView(ListView):
        model=Agreement
        context_object_name = "Agreements_list"


@login_required
def AgreementDetail(request,ag_id):
    actual_agreement = Agreement.objects.get(id=ag_id)
    agreement_balance = AgreementBalance.objects.get(name=actual_agreement)

    return render (request, 'balances/agreement_detail.html',{'agreement':actual_agreement,

                                                                'balance':agreement_balance})
@login_required
def counters(request):

    if request.method == 'POST':
        form = GetCountersData(request.POST)
        if form.is_valid():
            counters = CounterStatus()
            data_fields = ['gas1','gas2','gas3','electricity1','electricity2','electricity22','electricity3','electricity4','electricity5','water1','water2','water3','water4','water5','water_garden','waterh3','waterh4','waterh5','electricity_adm']
            for field in data_fields:
                setattr(counters,field,form.cleaned_data[field])

            counters.date=date.today()
            counters.save()

            return HttpResponseRedirect('/done')
    else:

        form=GetCountersData()

    return render (request, 'balances/counters.html',{'form':form})

@login_required
def done(request):

    pass

    return render(request, 'balances/done.html',{})

@login_required
def update_payments(request):
    history,user = get_history()
    history2=get_history2()
    update_payment(history,history2)

    return render(request, 'balances/done.html',{})

@login_required
def update_balances_and_payments(request):
    make_archive_entry()
    update_balances(pepole_count())
    update_all()

    return render(request, 'balances/done.html',{})

@login_required
def send_mail(request):
    agreements= Agreement.objects.all()

    for agreement in agreements:
        balance = AgreementBalance.objects.get(name = agreement)
        mailto = agreement.email
        msg = ('\n\n '+agreement.name+
               '\n\n GAZ: '+"{:.2f}".format(balance.gas)+
                ' zł\n PRĄD: '+"{:.2f}".format(balance.electricity)+
                'zł\n WODA:  '+"{:.2f}".format(balance.water)+
                'zł\n INTERNET: '+"{:.2f}".format(balance.internet)+
                ' zł\n ŚMIECI: '+"{:.2f}".format(balance.trashes)+
               ' zł\n ŁĄCZNIE MEDIA:  '+ "{:.2f}".format(balance.total))
                #' zł\n bilans opłat czynszu w poprzednim miesiacu:  '+ "{:.2f}".format(balance.wplata_za_ostatni_miesiac)+
                #' zł\n bilans opłat za media na dzień dzisiejszy:  '+ "{:.2f}".format(balance.bilans)+'zl')
        send_email(mailto,msg)

    return render(request, 'balances/done.html',{})


@login_required
def archive(request):

    entrys=make_entry()

    return render(request, 'balances/archive.html',{'entrys':entrys})

@login_required
def archive_date(request,date_template):

    entrys=make_entry()
    balances_date_template = entrys[date_template]

    return render(request, 'balances/archive/archive_date.html',{'balances':balances_date_template,'date': date_template})


@login_required
def archive_date_detail(request,date_template,name):

    entrys=make_entry()
    balances_date_template = entrys[date_template]
    for balance in balances_date_template:
        if str(balance.name)==str(name):
            balance_detail=balance
        else:
            pass
            
    return render(request, 'balances/archive/archive_date_detail.html',{'balance':balance_detail})