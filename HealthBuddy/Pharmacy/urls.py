from django.urls import path
from . import views

app_name = "Pharmacy"

urlpatterns = [
    path('', views.searchPres, name="searchPres"),
    path('pres/<int:patient_roll>/', views.presView, name="pres_empty"),
    path('pres/<int:patient_roll>/<int:pres_id>/', views.presView , name = "pres"),
    path('pres/change_quantity/<int:patient_roll>/<int:pres_id>/<int:med_id>/', views.change_quantity, name="change_quantity"),
    path('med_list/', views.med_list_view, name="med_list"),
    path('med_list/edit/<int:med_id>/<int:is_deleted>/', views.database, name="med_list_edit"),
    path('med_list/add_med/', views.add_new_med, name="add_new_med"),
    path('provided/<int:pres_id>/', views.verify_user, name="verify_user"),
]
