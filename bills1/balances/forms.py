from django import forms
from .models import CounterStatus
from django.utils.translation import ugettext_lazy as _

class GetCountersData(forms.ModelForm):

    class Meta:
        model =CounterStatus
        fields = ['gas1','gas2','gas3','electricity1','electricity2','electricity22','electricity3','electricity4','electricity5','water1','water2','water3','water4','water5','water_garden','waterh3','waterh4','waterh5','electricity_adm']
        labels = {
            'gas1': _('GAZ PARTER -JEDYNKA'),
            'gas2': _('GAZ PIĘTRO -DWÓJKA'),
            'gas3': _('GAZ DÓŁ -SUTERENA'),
            'electricity1': _('PRĄD PARTER -JEDYNKA'),
            'electricity2': _('PRĄD PIĘTRO G11 WYŻSZE WSKAZANIE'),
            'electricity22': _('PRĄD PIĘTRO G12 NIŻSZE WSKAZANIE'),
            'electricity3': _('PRĄD LIMONKA'),
            'electricity4': _('PRĄD TURKUSOWY RAJ'),
            'electricity5': _('PRĄD NASZE'),
            'water1': _('WODA PARTER -JEDYNKA'),   
            'water2': _('WODA PIĘTRO - DWÓJKA'),
            'water3': _('WODA ZIMNA LIMONKA'),
            'water4': _('WODA ZIMNA TURKUSOWY RAJ'),
            'water5': _('WODA ZIMNA NASZE'),
            'water_garden': _('WODA OGRÓD'),
            'waterh3': _('WODA CIEPŁA LIMONKA'),
            'waterh4': _('WODA CIPEŁA TURKUSOWY RAJ'),
            'waterh5': _('WODA CIPEŁA NASZE'),
            'electricity_adm': _('PRĄD ADMINISTRACYJNY NA DOLE'),
                 }
