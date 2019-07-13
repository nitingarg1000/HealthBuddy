from django.urls import path
from . import views

app_name = "Pharmacy"

urlpatterns = [
    path('pres/<int:patient_roll>/<int:pres_id>/', views.presView , name = "pres"),
    path('pres/change_quantity/<int:patient_roll>/<int:pres_id>/<int:med_id>/', views.change_quantity, name="change_quantity")
]