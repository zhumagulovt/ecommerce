from django import forms
from django.utils.translation import gettext_lazy as _


class RangeNumericForm(forms.Form):
    name = None

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super().__init__(*args, **kwargs)

        self.fields[self.name + '_from'] = forms.FloatField(label='', required=False,
            widget=forms.NumberInput(attrs={'placeholder': _('От')}))
        self.fields[self.name + '_to'] = forms.FloatField(label='', required=False,
            widget=forms.NumberInput(attrs={'placeholder': _('До')}))