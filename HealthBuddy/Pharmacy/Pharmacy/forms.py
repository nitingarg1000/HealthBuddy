from django import forms
from Doctor.models import PresMedicine
from .models import Medicine


class PharmacyPresForm(forms.ModelForm):

    class Meta:
        model = PresMedicine
        fields = ['provided']


class PharQuantity(forms.Form):
    quantity_provided = forms.IntegerField()


class PharMedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'quantity']

