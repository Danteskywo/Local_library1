from django import forms as f
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

class RenewBookForm(f.Form):
    renewal_date = f.DateField(
        help_text="Введите дату между сегодняшней и 4 неделями (по умолчанию 3).",
        widget=f.DateInput(attrs={'type': 'date'})
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата - продление в прошлом'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Неверная дата - продление более чем на 4 недели'))
        
        return data
