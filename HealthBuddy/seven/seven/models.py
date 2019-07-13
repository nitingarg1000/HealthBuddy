from django.db import models
from Doctor.models import Prescription


class TestPres(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    test = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    def __str__(self):
        return self.prescription.patient.user.username