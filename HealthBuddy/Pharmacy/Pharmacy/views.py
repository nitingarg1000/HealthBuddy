from django.shortcuts import render, get_object_or_404
from Doctor.models import PresMedicine, Prescription
from Patient.models import Patient
from .models import *
from .forms import PharQuantity
# Create your views here.


def presView(request, patient_roll, pres_id=None):
    form_class = PharQuantity
    patient = get_object_or_404(Patient, rollNo=patient_roll)
    pres = get_object_or_404(Prescription, pk=pres_id)
    med_list = Medicine.objects.all()
    med = PresMedicine.objects.filter(prescription=pres)
    form = form_class(request.POST or None)
    temp_list = []
    for m in med_list:
        for pm in med:
            if pm.medicine == m.name:
                temp_list.append(m)
    context = {
        'patient': patient,
        'pres': pres,
        'med_list': med_list,
        'med': med,
        'form': form,
        'temp_list': temp_list
    }

    return render(request, 'Pharmacy/pres_view.html', context)


def change_quantity(request, med_id, patient_roll, pres_id):
    form_class = PharQuantity
    template_name = 'Pharmacy/pres_view.html'
    patient = get_object_or_404(Patient, rollNo=patient_roll)
    pres = get_object_or_404(Prescription, pk=pres_id)
    med_list = Medicine.objects.all()
    med = PresMedicine.objects.filter(prescription=pres)
    form = form_class(request.POST or None)
    context = {
        'patient': patient,
        'pres': pres,
        'med_list': med_list,
        'med': med,
        'form': form,

    }

    if form.is_valid():
        q_changed = form.cleaned_data['quantity_provided']
        change_med_filter = Medicine.objects.filter(pk=med_id)
        change_med_get = Medicine.objects.get(pk=med_id)

        if q_changed <= change_med_get.quantity:
            new = change_med_get.quantity - q_changed
            change_med_filter.update(quantity = new)
            change_med_get.refresh_from_db()
            context['error_message'] = 'Quantity changed'
            form = form_class(None)
            context['form'] = form
            return render(request, template_name, context)
        else:
            context['error_message'] = 'Quantity not sufficient'
            form = form_class(None)
            context['form'] = form
            return render(request, template_name, context)

    context['error_message'] = 'Error: Quantity not changed'
    return render(request, template_name, context)


