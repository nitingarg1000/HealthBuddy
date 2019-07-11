from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from Doctor.models import Prescription
from Patient.models import Patient
import datetime

# Create your views here.

def delete_test(request, pres_id, testpres_id):
    pres = get_object_or_404(Prescription, pk=pres_id)
    testpres = get_object_or_404(TestPres, pk=testpres_id)
    patient = pres.patient
    form_class_testpres = TestPresForm
    template_name = 'seven/testpres_form.html'
    testpres_form = form_class_testpres(request.POST or None)
    testpres.delete()
    if testpres_form.is_valid():
        t = testpres_form.save(commit=False)
        t.save()
        testpres_form = form_class_testpres(None)
        return render(request, template_name,
                       {'testpres_form': testpres_form, 'error_message': 'Test Removed', 'pres': pres})
    testpres_form = form_class_testpres(None)
    return render(request, template_name,
                  {'testpres_form': testpres_form, 'error_message': 'Test Removed', 'pres': pres})


def add_test(request, pres_id, testpres_id=None):
    form_class_testpres = TestPresForm
    template_name = 'seven/testpres_form.html'
    pres = get_object_or_404(Prescription, pk=pres_id)
    patient = pres.patient

    if testpres_id is None:
        testpres_form = form_class_testpres(request.POST or None)
    else:
        testpres = get_object_or_404(TestPres, pk=testpres_id)
        testpres_form = form_class_testpres(request.POST or None, instance=testpres)

    if testpres_form.is_valid():
        if testpres_id is None:
            current_time = datetime.datetime.now()
            t = testpres_form.save(commit=False)
            t.date = current_time
            t.prescription = pres
            t.save()

            testpres_form = form_class_testpres(None)

            return render(request, template_name,
                        {'testpres_form': testpres_form, 'pres': pres, 'error_message': 'Form Saved', 'patient': patient})

    return render(request, template_name,
                  {'testpres_form': testpres_form, 'pres': pres, 'patient' : patient})
