from django import forms
from .models import TestPres


class TestPresForm(forms.ModelForm):

    class Meta:
        model = TestPres
        fields = ['test', 'value']

