from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views, logout

app_name = "users"
urlpatterns = [
    path('', views.Home.as_view(), name = "home"),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('register/stff_patient/', views.StffPatientRegFormView.as_view(), name="stff_pat_register"),
    path('register/stud_patient/', views.StudPatientRegFormView.as_view(), name="stud_pat_register"),
    path('healthcalc/', views.Calc.as_view(), name = "calc"),
    path('contact_us/', views.Contact.as_view(), name = "contact"),
    path('profile/', views.Profile.as_view(), name = "profile" ),
    path('login_user/', views.login_user, name = 'login_user'),
    path('logout/', views.logout_user, name = 'logout'),
    path('home/', views.redirect_home, name='redirect_home'),
    path('info/', views.HC_Info.as_view(), name = 'HC_Info'),
    #path('auth/', include('django.contrib.auth.urls')),
    # auth/login/ [name='login']
    # auth/logout/ [name='logout']
    # auth/password_change/ [name='password_change']
    # auth/password_change/done/ [name='password_change_done']
    # auth/password_reset/ [name='password_reset']
    # auth/password_reset/done/ [name='password_reset_done']
    # auth/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # auth/reset/done/ [name='password_reset_complete']
]
