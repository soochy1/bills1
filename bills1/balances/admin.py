from django.contrib import admin
from .models import Agreement,Payment,Payment_bills,AgreementBalance,AgreementBalance_archive,CounterStatus,Bills_prices,Account_details

admin.site.register([Agreement,Payment,Payment_bills,AgreementBalance,AgreementBalance_archive,CounterStatus,Bills_prices,Account_details])

# Register your models here.
