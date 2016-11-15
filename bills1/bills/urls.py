"""bills URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from balances import views
from balances.views import index,archive_date,archive_date_detail,AgreementListView,AgreementDetail,update_payments,update_balances_and_payments,send_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import  login,logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    url(r'^agreements/$',login_required(AgreementListView.as_view()),),
    url(r'^agreements/agreement_detail/(?P<ag_id>\w+)/$',views.AgreementDetail),
    url(r'^counters/$',views.counters),
    url(r'^done/$',views.done),
    url(r'^update_payments/$', views.update_payments),
    url(r'^update_balances/$',views.update_balances_and_payments),
    url(r'^mail/$',views.send_mail),
    url(r'^archive/$', views.archive),
    url(r'^archive/(?P<date_template>[0-9-]+)/$', views.archive_date),
    url(r'^archive/(?P<date_template>[0-9-]+)/(?P<name>\w+)/$', views.archive_date_detail),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
]
