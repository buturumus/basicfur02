from django import forms
from primepage.models import Partner
from primepage.models import Material
from primepage.models import MATRIX_CONSTS


class EditPartnerForm(forms.ModelForm):

    class Meta:
        model = Partner
        fields = (
            MATRIX_CONSTS['edit']['shown_keys'][Partner]
        )


class EditMaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = MATRIX_CONSTS['edit']['shown_keys'][Material]
