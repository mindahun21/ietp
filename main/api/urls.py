from . import views
from django.urls import path


urlpatterns = [
  path('login/', views.CustomLoginView.as_view(), name='login'),
  path('logout/', views.LogoutView.as_view(), name='api_logout'),
  path('patients/', views.PatientListView.as_view(), name='patient-list'),
  path('patient/<int:id>/case/', views.CaseDetailView.as_view(), name='case-detail'),
  path('case/<int:id>/checkups/', views.CheckupsView.as_view(), name='checkup-detail'),
  path('case/<int:id>/add-checkup/', views.AddCheckUpView.as_view(), name='add-checkup'),
]