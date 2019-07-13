from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import Appointment
from Patient.models import Patient
from students.models import students
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

            return redirect('/home/')

        else:
            a = form.save(commit=False)
            a.reqApproval = True
            # a.receptionist = receptionist
            a.dateNtime = datetime.datetime.now()
            a.save()

            return redirect('/home/')

    return redirect('/home/')

@login_required(login_url='/')
def clearList(request):
    if request.user.type.types == 'rec':
        Appointment.objects.filter(status='t').delete()
        return redirect('/home/')
    else:
        return render(request, 'users/home_base.html', {'error_message' : 'You are not authorised to perform this action'})


@login_required(login_url="/")
def approve(request, app_id):
    form_class = ApproveForm
    app = get_object_or_404(Appointment, pk=app_id)
    form = form_class(request.POST or None, instance=app)
    if form.is_valid():
        a = form.save(commit=False)
        a.reqApproval = True
        a.dateNtime = datetime.datetime.now()
        a.save()

        return redirect('/home/')

    return render(request, 'Reception/approve_form.html', {'form': form, 'a': app})


@login_required(login_url="/")
def pat_list(request):
    pat_list = Patient.objects.all()
    return render(request, 'Reception/patient_list.html', {'pat_list': pat_list})


@login_required(login_url="/")
def stud_list(request):
    stud_list = students.objects.all()
    return render(request, 'Reception/student_list.html', {'stud_list': stud_list})
