from django.contrib import messages
from .forms import AddEditPatientForm
from .models import Patient

from django.views.generic.detail import DetailView
from .models import Patient
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Patient
from .forms import AddEditPatientForm
from django.db import models

class CreatePatientView(CreateView):
    model = Patient
    form_class = AddEditPatientForm
    template_name = 'core/add_edit_model.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        context['model_name'] = 'Patient'
        context['action_url'] = '/patients/add/'
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.cases.create(status='open')
        messages.success(self.request, 'New Patient Added Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.id})


class UpdatePatientView(UpdateView):
    model = Patient
    form_class = AddEditPatientForm
    template_name = 'core/add_edit_model.html'

    def get_object(self):
        return get_object_or_404(Patient, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Patient'
        context['action_url'] = '/patients/edit/' + str(self.object.id) + '/'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Patient Data Edited Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.id})


class PatientDetailView(DetailView):
  template_name = 'patients/patients_detail.html'
  model = Patient
  context_object_name = 'patient'
  lookup_field = 'id'

  def get_object(self):
    patient= get_object_or_404(
        Patient.objects.select_related('medical_history'),
        id=self.kwargs.get(self.lookup_field)
        )
    assigned_nurses = patient.assigned_nurses.all()
    patient.assigned_nurses_list = assigned_nurses
    patient.cases_ordered = patient.cases.all().order_by(
        models.Case(
            models.When(status='open', then=0),
            models.When(status='closed', then=1),
        ),
        '-start_date'
    )
    return patient
  

from core.models import MedicalHistory
from .forms import MedicalHistoryForm
class CreateMedicalHistoryView(CreateView):
    template_name = 'core/add_edit_model.html'
    form_class = MedicalHistoryForm
    model = MedicalHistory
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        context['model_name'] = 'Medical History'
        context['action_url'] = '/patients/create-medical-history/' + str(self.kwargs.get('id')) + '/'
        return context

    def form_valid(self, form):
        patient  = get_object_or_404(Patient, id=self.kwargs.get('id'))

        self.object = form.save(commit=False)
        self.object.patient = patient
        self.object.save()
        print(form.cleaned_data)
        messages.success(self.request, 'New Medical History Added Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})
    
class UpdateMedicalHistoryView(UpdateView):
    template_name = 'core/add_edit_model.html'
    form_class = MedicalHistoryForm
    model = MedicalHistory
    def get_object(self):
        return get_object_or_404(MedicalHistory, id=self.kwargs.get('id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Medical History'
        context['action_url'] = '/patients/update-medical-history/' + str(self.object.id) + '/'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Medical History Edited Successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})
    

from .models import Insurance
from .forms import InsuranceInfoForm

class CreateInsuranceInfoView(CreateView):
    template_name = 'core/add_edit_model.html'
    form_class = InsuranceInfoForm
    model = Insurance
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        context['model_name'] = 'Insurance Info'
        context['action_url'] = '/patients/create-insurance-info/' + str(self.kwargs.get('id')) + '/'
        return context
    
    def form_valid(self, form):
        patient  = get_object_or_404(Patient, id=self.kwargs.get('id'))
        self.object = form.save(commit=False)
        self.object.patient = patient
        self.object.save()
        messages.success(self.request, 'New Insurance Info Added Successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})

class UpdateInsuranceInfoView(UpdateView):


    template_name = 'core/add_edit_model.html'
    form_class = InsuranceInfoForm
    model = Insurance
    def get_object(self):
        return get_object_or_404(Insurance, id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Insurance Info'
        context['action_url'] = '/patients/update-insurance-info/' + str(self.object.id) + '/'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Insurance Info Edited Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})
    

from core.models import Case
def CreateEmptyCase(request, id):
    patient = get_object_or_404(Patient, id=id)
    is_any = Case.objects.filter(patient=patient, status='open').exists()

    context = {}
    
    if is_any:
        messages.error(request, 'Patient already has an open case.')
        context['message'] = 'Patient already has an open case.'
    else:
        Case.objects.create(patient=patient, status='open')
        patient.is_active = True
        patient.save()
        context['message'] = 'New case created successfully.'
    
    patient.cases_ordered = patient.cases.all().order_by(
        models.Case(
            models.When(status='open', then=0),
            models.When(status='closed', then=1),
        ),
        '-start_date'
    )
    context['patient'] = patient
    
    return render(request, 'partials/cases_table.html', context)


class CaseDetailView(DetailView):
    model = Case
    template_name = 'patients/case_detail.html'
    context_object_name = 'case'
    lookup_field = 'id'


    def get_object(self):
        case_obj = get_object_or_404(
            Case.objects.prefetch_related(
                'checkups',
                models.Prefetch(
                    'treatments',
                    queryset=Treatment.objects.prefetch_related(
                        'lab_results',
                        'immunizations'
                    )
                )
              ),
            id=self.kwargs.get('id')
          )
        case_obj.checkups_ordered = case_obj.checkups.order_by('-date', '-time')
        return case_obj
    
    # def get(self, request, *args, **kwargs):
    #     case = self.get_object()
    #     context = self.get_context_data(object=case)
    #     return render(request, self.template_name, context)


def CloseCaseView(request, id):
    case = get_object_or_404(Case, id=id)
    case.close_case()
    patient = get_object_or_404(Patient, id=case.patient.id)
    patient.is_active = False
    patient.assigned_nurses.clear()
    if patient.bed:
        bed = patient.bed
        bed.status = 'available'
        bed.save()
        patient.bed = None
    patient.save()

    messages.success(request, 'Case Closed Successfully.')
    return redirect('patient-detail', id=case.patient.id)


from .forms import InitialDiagnosisForm
class UpdateInitialDiagnosisView(UpdateView):
    template_name = 'core/add_edit_model.html'
    form_class = InitialDiagnosisForm
    model = Case
    def get_object(self):
        return get_object_or_404(Case, id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Initial Diagnosis'
        context['action_url'] = '/patients/update-initial-diagnosis/' + str(self.kwargs.get('id')) + '/'
        return context

    def form_valid(self, form):
        case_obj = get_object_or_404(Case, id=self.kwargs.get('id'))
        case_obj.initial_diagnosis = form.cleaned_data['initial_diagnosis']
        messages.success(self.request, 'Initial Diagnosis Edited Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})


from .forms import TreatmentPlanForm
class UpdateTreatmentPlanView(UpdateView):
    template_name = 'core/add_edit_model.html'
    form_class = TreatmentPlanForm
    model = Case
    def get_object(self):
        return get_object_or_404(Case, id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Treatment Plan'
        context['action_url'] = '/patients/update-treatment-plan/' + str(self.kwargs.get('id')) + '/'
        return context
    
    def form_valid(self, form):
        case_obj = get_object_or_404(Case, id=self.kwargs.get('id'))
        case_obj.treatment_plan = form.cleaned_data['treatment_plan']
        messages.success(self.request, 'Treatment Plan Edited Successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})


from .forms import ClosureInfoForm
class UpdateClosureInfoView(UpdateView):
    template_name = 'core/add_edit_model.html'
    form_class = ClosureInfoForm
    model = Case
    def get_object(self):
        return get_object_or_404(Case, id=self.kwargs.get('id'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Closure Info'
        context['action_url'] = '/patients/update-closure-info/' + str(self.kwargs.get('id')) + '/'
        return context
    
    def form_valid(self, form):
        case_obj = get_object_or_404(Case, id=self.kwargs.get('id'))
        case_obj.closure_info = form.cleaned_data['closure_info']
        messages.success(self.request, 'Closure Info Edited Successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})


from .forms import NotesForm
class UpdateNotesView(UpdateView):
    template_name = 'core/add_edit_model.html'
    form_class = NotesForm
    model = Case
    def get_object(self):
        return get_object_or_404(Case, id=self.kwargs.get('id'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Notes'
        context['action_url'] = '/patients/update-notes/' + str(self.kwargs.get('id')) + '/'
        return context

    def form_valid(self, form):
        case_obj = get_object_or_404(Case, id=self.kwargs.get('id'))
        case_obj.notes = form.cleaned_data['notes']
        messages.success(self.request, 'Notes Edited Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.patient.id})
    


from core.models import CheckUp
from .forms import CheckUpForm
class CreateCheckUpView(CreateView):
    model = CheckUp
    form_class = CheckUpForm
    template_name = 'core/add_edit_model.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        context['model_name'] = 'Check Up'
        context['action_url'] = '/patients/add-check-up/'+ str(self.kwargs.get('id')) + '/'
        return context
    
    def form_valid(self, form):
        case_obj = get_object_or_404(Case, id=self.kwargs.get('id'))
        self.object = form.save(commit=False)
        self.object.case = case_obj
        self.object.save()
        messages.success(self.request, 'Check Up Added Successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.case.patient.id})
    

from core.models import Treatment
from .forms import TreatmentForm
class CreateTreatmentView(CreateView):
    model = Treatment
    form_class = TreatmentForm
    template_name = 'core/add_edit_model.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        context['model_name'] = 'Treatment'
        context['action_url'] = '/patients/add-treatment/'+ str(self.kwargs.get('id')) + '/'
        return context
    
    def form_valid(self, form):
        case_obj = get_object_or_404(Case, id=self.kwargs.get('id'))
        self.object = form.save(commit=False)
        self.object.case = case_obj
        self.object.doctor = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.case.patient.id})
    

from .forms import AssignNursesForm
class AssignNursesView(UpdateView):
    model = Patient
    template_name = 'core/add_edit_model.html'
    form_class = AssignNursesForm
    def get_object(self):
        return get_object_or_404(Patient, id=self.kwargs.get('id'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Assign Nurses'
        context['action_url'] = '/patients/assign-nurses/' + str(self.kwargs.get('id')) + '/'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Nurses Assigned Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.object.id})
    
    
from .forms import AssignBedForm
from django.views.generic.edit import FormView

class AssignBedView(FormView):
    template_name = 'core/add_edit_model.html'
    form_class = AssignBedForm

    def get_object(self):
        return get_object_or_404(Patient, id=self.kwargs.get('id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['model_name'] = 'Assign Bed'
        context['action_url'] = '/patients/assign-bed/' + str(self.kwargs.get('id')) + '/'
        return context
    def form_valid(self, form):
        patient = self.get_object()
        new_bed = form.cleaned_data['bed']
        if patient.bed:
            patient.bed.status = 'available'
            patient.bed.save()
        
        patient.bed = new_bed
        patient.save()

        new_bed.status = 'occupied'
        new_bed.save()

        messages.success(self.request, 'Bed Assigned Successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient-detail', kwargs={'id': self.kwargs.get('id')})
