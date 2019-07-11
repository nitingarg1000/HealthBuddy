from django.shortcuts import render, get_object_or_404, redirect
from .forms import AppointmentForm
from .models import Appointment
from Patient.models import Patient
import datetime
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


@login_required(login_url = "/")
class ReceptionHome(TemplateView):
    template_name = ""


@login_required(login_url = "/")
def create_appointment(request, app_id=None):
    template_name = ""
    receptionist = request.user.reception
    form_class = AppointmentForm
    if app_id is None:
        form = form_class(request.POST or None)
    else:
        app = get_object_or_404(Appointment, pk=app_id)
        form = form_class(request.POST or None, instance=app)

    if form.is_valid():
        if app_id is None:
            a = form.save(commit=False)
            a.reqApproval = True
            a.patient = Patient.objects.get(pk=a.patient_roll)
            # a.receptionist = receptionist
            a.dateNtime = datetime.datetime.now()
            a.save()

            return redirect('/login_user/')

        else:
            a = form.save(commit=False)
            a.reqApproval = True
            # a.receptionist = receptionist
            a.dateNtime = datetime.datetime.now()
            a.save()

            return redirect('/login_user/')

    return redirect('/login_user/')
