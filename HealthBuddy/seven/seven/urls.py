from django.urls import path
from . import views

app_name = "seven"

urlpatterns = [
    path('<int:pres_id>/', views.add_test, name='create_testpres'),
    path('<int:pres_id>/<int:testpres_id>/', views.add_test, name='change_testpres'),
    path('<int:pres_id>/delete_test/<int:testpres_id>/', views.delete_test, name="delete_test")
]