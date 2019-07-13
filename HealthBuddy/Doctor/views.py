from django.shortcuts import render, get_object_or_404
from .forms import *
from Patient.models import Patient
from .models import *
import datetime
from Reception.models import Appointment
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "Doctor/home_doc.html"

@login_required(login_url = "/")
#saves pres and renders reference form
def redirect_ref_form(request, patient_roll, pres_id=None):
    if request.user.type.types != 'doc':
        return render(request, 'users/base_home.html', {"error_message": "you are not autharised to view this page"})
    if pres_id:
        pres = get_object_or_404(Prescription, pk=pres_id)
        if pres.doctor.user.username != request.user.username:
            return render(request, 'users/base_home.html', {"error_message": "you are not autharised to view this page"})
    form_class_pres = PrescriptionForm
    form_class_med = PresMedicineForm
    template_name = 'Doctor/prescription_form.html'
    patient = get_object_or_404(Patient, pk=patient_roll)
    # app = Appointment.objects.filter(patient=patient)
    form_class = CreateReferForm
    form = form_class(None)

    if pres_id == None:
        pres_form = form_class_pres(request.POST or None)
        med_form = form_class_med(request.POST or None)
    else:
        pres = get_object_or_404(Prescription, pk=pres_id)
        pres_form = form_class_pres(request.POST or None, instance=pres)
        med_form = form_class_med(request.POST or None)

    if pres_form.is_valid():
        if pres_id == None:
            # current_time = datetime.datetime.now()
            p = pres_form.save(commit=False)
            # p.date = current_time
            p.doctor = request.user.doctor
            p.patient = patient
            p.med_added = True
            p.save()
            pres_form.save_m2m()
            current_time = datetime.datetime.now()
            det = PresDetails(date=current_time, pres=p, doctor=request.user.doctor)
            det.save()

            return render(request, 'Doctor/refer_form.html', {'form': form, 'pres': p})
        else:
            p = pres_form.save(commit=False)
            p.save()
            pres_form.save_m2m()
            current_time = datetime.datetime.now()
            det = PresDetails(date=current_time, pres=p, doctor=request.user.doctor)
            det.save()

            return render(request, 'Doctor/refer_form.html',{'form': form, 'pres': p})
    return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'patient': patient, 'error_message': 'Error: Invalid form submission, cannot create reference'})


@login_required(login_url = "/")
#delete appointment by filtering from patient and not by using app_id
def save_pres(request, patient_roll, pres_id=None, end=None):
    # if request.user.type.types != 'doc':
    #     return render(request, 'users/base_home.html', {"error_message" : "you are not autharised to view this page"})
    # if pres_id:
    #     pres = get_object_or_404(Prescription, pk=pres_id)
    #     if pres.doctor.user.username != request.user.username:
    #         return render(request, 'users/base_home.html', {"error_message" : "you are not autharised to view this page"})
    form_class_pres = PrescriptionForm
    form_class_med = PresMedicineForm
    template_name = 'Doctor/prescription_form.html'
    patient = get_object_or_404(Patient, pk=patient_roll)
    applist = Appointment.objects.filter(patient=patient)
    app = applist.reverse()[0]

    if pres_id == None:
        pres_form = form_class_pres(request.POST or None)
        med_form = form_class_med(request.POST or None)
    else:
        pres = get_object_or_404(Prescription, pk=pres_id)
        pres_form = form_class_pres(request.POST or None, instance=pres)
        med_form = form_class_med(request.POST or None)

    if pres_form.is_valid():
        if pres_id == None:
            p = pres_form.save(commit=False)
            p.doctor = request.user.doctor
            p.patient = patient
            p.med_added = True

            p.save()
            pres_form.save_m2m()
            # current_time = datetime.datetime.now()
            # det = PresDetails(date=current_time, pres=p, doctor=request.user.doctor)
            # det.save()
            med_form = form_class_med(None)
            pres_form = form_class_pres(None)
            app.status = 'e'
            app.save()
            if end:
                app.status = 't'
                app.save()
            return render(request, template_name,
                          {'pres_form': pres_form, 'med_form': med_form, 'patient': patient, 'error_message': 'form saved'})
        else:
            p = pres_form.save(commit=False)
            p.save()
            pres_form.save_m2m()
            current_time = datetime.datetime.now()
            time = PresDetails(date=current_time, pres=p, doctor=request.user.doctor)
            time.save()

            med_form = form_class_med(None)
            pres_form = form_class_pres(None)
            app.status = 'e'
            app.save()
            if end:
                # app.delete()
                app.status = 't'
                app.save()
            return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'patient': patient, 'error_message': 'form saved'})


    return render(request, template_name,{'pres_form': pres_form, 'med_form': med_form, 'patient': patient})

@login_required(login_url = "/")
def delete_med(request, patient_roll, pres_id, med_id):
    if request.user.type.types != 'doc':
        return render(request, 'users/base_home.html', {"error_message" : "you are not autharised to view this page"})
    if pres_id:
        pres = get_object_or_404(Prescription, pk=pres_id)
        if pres.doctor.user.username != request.user.username:
            return render(request, 'users/base_home.html', {"error_message" : "you are not autharised to view this page"})

    patient = get_object_or_404(Patient, pk=patient_roll)
    pres = get_object_or_404(Prescription, pk=pres_id)
    form_class_pres = PrescriptionForm
    form_class_med = PresMedicineForm
    template_name = 'Doctor/prescription_form.html'
    pres_form = form_class_pres(request.POST or None, instance=pres)
    med_form = form_class_med(None)
    med = PresMedicine.objects.get(pk=med_id)
    med.delete()
    if pres_form.is_valid():
        p = pres_form.save(commit=False)
        p.save()
        pres_form.save_m2m()
        return render(request, template_name,
                      {'pres_form': pres_form, 'med_form': med_form, 'pres': p, 'patient': patient,
                       'error_message': 'Medicine removed'})

    return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'pres': pres, 'patient': patient,
                                           'error_message': 'Medicine removed'})

@login_required(login_url = "/")
def add_med(request, patient_roll, pres_id=None):
    if request.user.type.types != 'doc':
        return render(request, 'users/base_home.html', {"error_message" : "you are not autharised to view this page"})
    if pres_id:
        pres = get_object_or_404(Prescription, pk=pres_id)
        if pres.doctor.user.username != request.user.username:
            return render(request, 'users/base_home.html', {"error_message" : "you are not autharised to view this page"})

    form_class_pres = PrescriptionForm
    form_class_med = PresMedicineForm
    template_name = 'Doctor/prescription_form.html'
    patient = get_object_or_404(Patient, pk = patient_roll)

    if pres_id == None:
        pres_form = form_class_pres(request.POST or None)
        med_form = form_class_med(request.POST or None)
    else:
        pres = get_object_or_404(Prescription, pk=pres_id)
        pres_form = form_class_pres(request.POST or None, instance=pres)
        med_form = form_class_med(request.POST or None)

    if pres_form.is_valid() and med_form.is_valid():
        if pres_id == None:
            # current_time = datetime.datetime.now()
            p = pres_form.save(commit=False)
            # p.date = current_time
            p.doctor = request.user.doctor
            p.patient = patient
            p.med_added = True
            # p.app
            p.save()
            pres_form.save_m2m()

            m = med_form.save(commit=False)
            m.prescription = p
            m.save()
            med_form = form_class_med(None)

            return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'pres': p, 'patient': patient, 'error_message': 'medicine added'})
        else:
            p = pres_form.save(commit=False)
            p.save()
            pres_form.save_m2m()

            m = med_form.save(commit=False)
            m.prescription = p
            m.save()
            med_form = form_class_med(None)

            return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'pres': p, 'patient': patient, 'error_message': 'medicine added'})

    return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'patient': patient})

@login_required(login_url = "/")
def create_reference(request, pres_id):
    if request.user.type.types != 'doc':
        return render(request, 'users/base_home.html', {"error_message": "you are not autharised to view this page"})
    if pres_id:
        pres = get_object_or_404(Prescription, pk=pres_id)
        if pres.doctor.user.username != request.user.username:
            return render(request, 'users/base_home.html', {"error_message": "you are not autharised to view this page"})

    form_class = CreateReferForm
    template_name = 'Doctor/refer_form.html'
    form = form_class(request.POST or None)
    doctor = request.user.doctor
    pres = get_object_or_404(Prescription, pk=pres_id)

    if form.is_valid():
        r = form.save(commit=False)
        r.from_doc = doctor
        r.prescription = pres
        r.save()

        return render(request, template_name, {'error_message': 'Reference saved!', 'pres': pres})

    return render(request, template_name, {'form': form, 'pres': pres})


def edit_pres(request, pres_id):
    pres = get_object_or_404(Prescription, pk=pres_id)
    doc = request.user.doctor
    form_class_pres = PrescriptionForm
    form_class_med = PresMedicineForm
    template_name = 'Doctor/prescription_form.html'
    patient = pres.patient
    med_form = form_class_med(None)
    pres_form = form_class_pres(None)
    #temp stores list of usernames of all users that have saved the prescription
    temp = []

    # for p in pres.presdetails_set.all():
    #     temp.append(p.doctor.user.username)

    # if request.user.username in temp:
    pres_form = form_class_pres(None, instance=pres)
    return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'patient': patient, 'pres': pres})

    return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'patient': patient, 'error_message': 'You do not have rights to edit this prescription.'})


def ref_pres(request, ref_id):
    ref = get_object_or_404(References, pk=ref_id)
    pres = ref.prescription

    form_class_pres = PrescriptionForm
    form_class_med = PresMedicineForm
    template_name = 'Doctor/prescription_form.html'
    patient = pres.patient
    med_form = form_class_med(None)
    pres_form = form_class_pres(None)

    if request.user.username == ref.to_doc.user.username:
        pres_form = form_class_pres(None, instance=pres)
        return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'patient': patient, 'pres': pres})

    return render(request, template_name, {'pres_form': pres_form, 'med_form': med_form, 'patient': patient, 'error_message': 'You do not have rights to edit this prescription.'})
