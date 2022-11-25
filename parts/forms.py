# parts/forms.py

# from django.db import models
from django import forms
from crispy_forms.helper import FormHelper
from primepage.models import Partner
from primepage.models import Material
# from primepage.models import MoneyEntry
from primepage.models import MoneyEntriesBunch


class EditPartnerForm(forms.ModelForm):

    class Meta:
        model = Partner
        fields = (
            Partner.MATRIX_CONSTS['edit']['shown_keys']
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class EditMaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = Material.MATRIX_CONSTS['edit']['shown_keys']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


"""
class EditMoneyEntryForm(forms.ModelForm):

    class Meta:
        model = MoneyEntry
        fields = (
            MoneyEntry.MATRIX_CONSTS['edit']['shown_keys']
        )
        widgets = {
            'humanid': forms.TextInput(attrs={'disabled': True}),
            'create_date': forms.DateTimeInput(attrs={'disabled': True}),
            'created_by': forms.Select(attrs={'disabled': True}),
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
            'hot_entry': forms.Select(attrs={'disabled': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
"""


class EditMoneyEntriesBunchForm(forms.ModelForm):

    class Meta:
        model = MoneyEntriesBunch
        fields = (
            MoneyEntriesBunch.MATRIX_CONSTS['edit']['shown_keys']
        )
        widgets = {
            'humanid': forms.TextInput(attrs={'disabled': True}),
            'create_date': forms.DateTimeInput(
                attrs={'disabled': True, 'class': 'text-center'},
            ),
            'created_by': forms.Select(attrs={'disabled': True}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hot_entry': forms.Select(attrs={'disabled': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

