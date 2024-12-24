from . import views
from django.urls import path


urlpatterns = [
  path('add/', views.CreatePatientView.as_view(), name='add-patient'),
  path('edit/<int:id>/', views.UpdatePatientView.as_view(), name='edit-patient'),
  path('patient-detail/<int:id>/', views.PatientDetailView.as_view(), name='patient-detail'),
  path('create-medical-history/<int:id>/', views.CreateMedicalHistoryView.as_view(), name='create-medical-history'),
  path('update-medical-history/<int:id>/', views.UpdateMedicalHistoryView.as_view(), name='update-medical-history'),
  path('update-insurance-info/<int:id>/', views.UpdateInsuranceInfoView.as_view(), name='update-insurance-info'),
  path('create-insurance-info/<int:id>/', views.CreateInsuranceInfoView.as_view(), name='create-insurance-info'),
  path('create-new-case/<int:id>/', views.CreateEmptyCase, name='create-new-case'),
  path('case-detail/<int:id>/', views.CaseDetailView.as_view(), name='case-detail'),
  path('close-case/<int:id>/', views.CloseCaseView, name='close-case'),
  path('update-initial-diagnosis/<int:id>/', views.UpdateInitialDiagnosisView.as_view(), name='update-initial-diagnosis'),
  path('update-treatment-plan/<int:id>/', views.UpdateTreatmentPlanView.as_view(), name='update-treatment-plan'),
  path('update-closure-info/<int:id>/', views.UpdateClosureInfoView.as_view(), name='update-closure-info'),
  path('update-notes/<int:id>/', views.UpdateNotesView.as_view(), name='update-notes'),
  path('add-check-up/<int:id>/', views.CreateCheckUpView.as_view(), name='add-check-up'),
  path('add-treatment/<int:id>/', views.CreateTreatmentView.as_view(), name='add-treatment'),
  path('assign-nurses/<int:id>/', views.AssignNursesView.as_view(), name='assign-nurses'),
]

# TODO: create edit for medical history
# TODO: create edit, enter closure info for Case
# TODO: create edit for Treatment in the case
# TODO: create edit for Lab result in the treatment
# TODO: create edit for Immunization in the treatment

