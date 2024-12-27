from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from patients.models import Patient
from patients.filters import PatientFilter
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.template.loader import render_to_string


from .forms import StaffAddForm


User = get_user_model()

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is an admin
        if request.user.is_authenticated:
            if request.user.role != 'admin':
                logout(request)
                # Show a message informing the user
                messages.warning(request, "This page is for admins only.")
                return redirect('/login')
        else:
            return redirect('/login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        patients = Patient.objects.all()
        patient_filter = PatientFilter(self.request.GET, queryset=patients)

        paginator = Paginator(patient_filter.qs, 25)  # Show 25 patients per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        start_index = (page_obj.number - 1) * 25

        context['filters'] = patient_filter
        context['patients'] = page_obj
        context['start_index'] = start_index
        return context

    def render_to_response(self, context, **response_kwargs):
        # Return only the patients list if this is an HTMX request
        if self.request.htmx:
            return HttpResponse(
                render_to_string('patients/patients_list.html', context),
                content_type="text/html",
            )
        return super().render_to_response(context, **response_kwargs)


User = get_user_model()

class StaffRegisterView(CreateView):
    template_name = 'core/add_edit_model.html'
    form_class = StaffAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        context['model_name'] = 'Staff'
        context['action_url'] = '/add-staff/'
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'New Staff Added Successfully. you can add another staff')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')
    


class LoginView(TemplateView):
    template_name = 'core/login.html'

    def get(self, request, *args, **kwargs):
      if request.user.is_authenticated:
          return redirect('/')
      return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            print('authenticated ------------')
            login(self.request, user)
            
            return redirect('/')
        else:
            print('not authenticated ------------')
            return render(self.request, self.template_name, {'error': 'Invalid username or password. Please try again.'})

class LogoutView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login')


class StaffDetailView(DetailView):
    model = User
    template_name = 'core/staff_detail.html'
    context_object_name = 'staff'
    lookup_field = 'id'

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs.get(self.lookup_field))