from django.urls import path
from . import views

urlpatterns =[
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login-template'),
    path('add-staff/', views.StaffRegisterView.as_view(), name='add-staff'),
    path('staff-detail/<int:id>/',views.StaffDetailView.as_view(),name='staff-detail'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
 

# TODO: give assign the doctor and nurses for the patient
# TODO: finish checkup models