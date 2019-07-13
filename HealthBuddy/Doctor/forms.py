from django import forms
from .models import *

class PrescriptionForm(forms.ModelForm):


    class Meta:
        model = Prescription
        fields = ['treatmentFor' ,'tests', 'roomNo7', 'remarks']

class PresMedicineForm(forms.ModelForm):

    class Meta:
        model = PresMedicine
        fields = ['medicine', 'times_a_day', 'no_of_days', 'when_to_take']

class CreateReferForm(forms.ModelForm):

    class Meta:
        model = References
        fields = ['to_doc', 'remarks_from_doc']
