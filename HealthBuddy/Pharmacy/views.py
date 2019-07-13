from django.shortcuts import render, get_object_or_404
from Doctor.models import PresMedicine, Prescription
from Patient.models import Patient
from .models import *
from .forms import PharQuantity, PresSearch
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/")
def searchPres(request):
    form_class = PresSearch
    form = form_class(request.POST or None)
    if form.is_valid():
        roll = form.cleaned_data['patient_roll']
        patient = get_object_or_404(Patient, pk=roll)
        med_list = Medicine.objects.all()
        form_class1 = PharQuantity
        form1 = form_class1(request.POST or None)
        context = {
            'form': form1,
            'med_list': med_list,
            'patient': patient
        }
        return render(request, 'Pharmacy/pres_view.html', context)

    return render(request, 'Pharmacy/phar_base.html', {'form': form})


@login_required(login_url="/")
def verify_user(request, pres_id):
    pres = get_object_or_404(Prescription, pk=pres_id)
    med = PresMedicine.objects.filter(prescription=pres)
    med_list_all = Medicine.objects.all()
    username = request.POST['username']
    password = request.POST['password']
    provided = request.POST.getlist('provided')

    patient = pres.patient
    form_class = PharQuantity
    form = form_class(None)
    temp_list = []
    for m in med_list_all:
        for pm in med:
            if pm.medicine == m.name:
                temp_list.append(m)

    user = authenticate(username=username, password=password)
    if user is not None:
        med_list = []
        for med in provided:
            m = get_object_or_404(PresMedicine, pk=med)
            med_list.append(m)

        for med in med_list:
            med.provided = True
            med.save()

        context = {
            'patient': patient,
            'pres': pres,
            'med_list': med_list_all,
            'med': med,
            'form': form,
            'temp_list': temp_list,
            'error_message': 'Medicine provided',
        }

        return render(request, 'Pharmacy/test.html', {'med_list': med_list})
    else:
        context = {
            'patient': patient,
            'pres': pres,
            'med_list': med_list_all,
            'med': med,
            'form': form,
            'temp_list': temp_list,
            'error_message': 'Invalid login',
        }

        return render(request, 'Pharmacy/pres_view.html', context)


@login_required(login_url="/")
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


@login_required(login_url="/")
def change_quantity(request, med_id, patient_roll, pres_id):
    form_class = PharQuantity
    template_name = 'Pharmacy/pres_view.html'
    patient = get_object_or_404(Patient, rollNo=patient_roll)
    pres = get_object_or_404(Prescription, pk=pres_id)
    med_list = Medicine.objects.all()
    med = PresMedicine.objects.filter(prescription=pres)
    form = form_class(request.POST or None)
    temp_list = []

    if form.is_valid():
        q_changed = form.cleaned_data['quantity_provided']
        change_med_get = Medicine.objects.get(pk=med_id)

        if q_changed <= change_med_get.quantity:
            new = change_med_get.quantity - q_changed
            change_med_get.quantity = new
            change_med_get.save()
            change_med_get.refresh_from_db()
            form = form_class(None)
            temp_list = []
            for m in med_list:
                for pm in med:
                    if pm.medicine == m.name:
                        temp_list.append(m)
            a = {'error_message': 'Quantity changed', 'patient': patient, 'pres': pres, 'med_list': med_list,
                 'med': med, 'temp_list': temp_list, 'form': form}
            return render(request, template_name, a)
        else:
            for m in med_list:
                for pm in med:
                    if pm.medicine == m.name:
                        temp_list.append(m)
            form = form_class(None)
            context = {
                'patient': patient,
                'pres': pres,
                'med_list': med_list,
                'med': med,
                'form': form,
                'temp_list': temp_list,
                'error_message': 'Quantity not sufficient'

            }

            return render(request, template_name, context)

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

    return render(request, template_name, context)

@login_required(login_url="/")
def database(request, med_id, is_deleted):
    form_class = PharQuantity
    template_name = 'Pharmacy/med_list.html'

    med_list = Medicine.objects.all()
    form = form_class(request.POST or None)

    if form.is_valid():
        q_changed = form.cleaned_data['quantity_provided']
        change_med_get = Medicine.objects.get(pk=med_id)

        if is_deleted:
            if q_changed <= change_med_get.quantity:
                new = change_med_get.quantity - q_changed
            else:
                form = form_class(None)
                context = {
                    'med_list': med_list,
                    'form': form,
                    'error_message': 'Quantity not sufficient',
                    'med_form': PharMedicineForm(None)
                }

                return render(request, template_name, context)

        else:
            new = change_med_get.quantity + q_changed

        change_med_get.quantity = new
        change_med_get.save()
        change_med_get.refresh_from_db()
        form = form_class(None)
        a = {'error_message': 'Quantity changed', 'med_list': med_list, 'form': form,
             'med_form': PharMedicineForm(None)}
        return render(request, 'Pharmacy/med_list.html', a)

    context = {
        'med_list': med_list,
        'form': form,
        'error_message': "quantity not changed.",
        'med_form': PharMedicineForm(None)
    }

    return render(request, template_name, context)

@login_required(login_url="/")
def med_list_view(request):
    med_list = Medicine.objects.all()
    return render(request, 'Pharmacy/med_list.html',
                  {'med_list': med_list, 'form': PharQuantity(None), 'med_form': PharMedicineForm(None)})

@login_required(login_url="/")
def add_new_med(request):
    form_class = PharMedicineForm
    form = form_class(request.POST or None)
    med_list = Medicine.objects.all()
    if form.is_valid():
        f = form.save()

        return render(request, 'Pharmacy/med_list.html',
                      {'med_list': med_list, 'form': PharQuantity(None), 'med_form': form})
    return render(request, 'Pharmacy/med_list.html',
                  {'med_list': med_list, 'form': PharQuantity(None), 'med_form': form,
                   'error': 'Couldn\'t add medicine'})



