from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Client, Case, Lawyer  , Vendor
from .forms import ClientForm, LawyerForm, CaseForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CaseForm,HearingFormSet
from .models import Case
from django.forms import inlineformset_factory
from .models import Case, Document,Hearing
from .forms import CaseForm, DocumentFormSet

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django_filters.views import FilterView
from .models import Case
from .filters import CaseFilter

# ✅ User Login View (Uses Django's built-in login)
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Create this template
    redirect_authenticated_user = True  # If logged in, go to home page
    success_url = '/'  # Redirect after login

# ✅ User Logout View
class CustomLogoutView(LogoutView):
    next_page = '/'  # Redirect to home page after logout

# ✅ User Registration View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('cases:case_list')  # ✅ Redirect to cases list after signup
        else:
            print("Form Errors:", form.errors)  # ✅ Debugging: Print errors if form is invalid
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('case_list')  # Adjust the redirect as needed
    else:
        form = CaseForm()
    return render(request, 'add_case.html', {'form': form})

def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_detail', case_id=case.id)  # Adjust the redirect as needed
    else:
        form = CaseForm(instance=case)
    return render(request, 'edit_case.html', {'form': form})

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tomorrow = timezone.now().date() + timedelta(days=1)
        
        context['clients_count'] = Client.objects.count()
        context['lawyers_count'] = Lawyer.objects.count()
        context['cases_count'] = Case.objects.count()
        context["vendors_count"] = Vendor.objects.count()
        context['upcoming_hearings'] = Hearing.objects.filter(hearing_date__date=tomorrow)

        return context

# Client views

class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("cases:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("cases:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("cases:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Client"
        return context


# Lawyer Views

class LawyerListView(ListView):
    model = Lawyer
    template_name = "lawyers/lawyer_list.html"


class LawyerCreateView(CreateView):
    model = Lawyer
    form_class = LawyerForm
    template_name = 'lawyers/lawyer_form.html'
    success_url = reverse_lazy('cases:lawyer_list')

    # Remove ALL custom logic from form_valid
    def form_valid(self, form):
        return super().form_valid(form)  # Let Django handle saving

class LawyerUpdateView(UpdateView):
    model = Lawyer
    form_class = LawyerForm
    template_name = "lawyers/lawyer_form.html"
    success_url = "/lawyers/"


class LawyerDeleteView(DeleteView):
    model = Lawyer
    template_name = "lawyers/lawyer_confirm_delete.html"
    success_url = reverse_lazy("cases:lawyer_list")


from django.db.models import Q
from django_filters.views import FilterView

class CaseListView(LoginRequiredMixin, FilterView, ListView):
    model = Case
    template_name = "cases/case_list.html"
    context_object_name = "cases"
    ordering = ["-created_at"]
    login_url = "cases:login"
    filterset_class = CaseFilter

    def get_queryset(self):
        """Apply both search query and filters."""
        queryset = super().get_queryset().prefetch_related("hearings")

        # Apply filters from CaseFilter
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs  # Use the filtered queryset

        # Apply search query
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(status__icontains=search_query)
                | Q(client__first_name__icontains=search_query)
                | Q(client__last_name__icontains=search_query)
                | Q(client__email__icontains=search_query)
                | Q(client__phone__icontains=search_query)
                | Q(lawyer__first_name__icontains=search_query)
                | Q(lawyer__last_name__icontains=search_query)
                | Q(lawyer__email__icontains=search_query)
                | Q(lawyer__phone__icontains=search_query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        """Pass filters and search to the template."""
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset  # Pass the filter object to the template

        # Pass filter values for dropdowns
        context["statuses"] = Case.objects.values_list("status", flat=True).distinct()
   #     context["lawyers"] = Case.objects.values_list("lawyer__first_name", "lawyer__last_name", "lawyer__id").distinct()
        context["clients"] = Case.objects.values_list("client__first_name", "client__last_name", "client__id").distinct()

        return context




def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            # Add debug print before saving
            print("Form is valid. Attempting to save...")
            try:
                case = form.save()
                print(f"Successfully saved case ID {case.id}")
                return redirect('cases:case_list')
            except Exception as e:
                print(f"Error saving case: {str(e)}")
                form.add_error(None, f"Error saving case: {str(e)}")
        else:
            # Print detailed form errors
            print("Form invalid. Errors:")
            for field, errors in form.errors.items():
                print(f"{field}: {', '.join(errors)}")
    else:
        form = CaseForm()
    
    return render(request, 'cases/case_form.html', {'form': form})
def case_documents(request, pk):
    case = get_object_or_404(Case, pk=pk)
    documents = Document.objects.filter(case=case)
    return render(request, 'cases/documents_list.html', {
        'case': case,
        'documents': documents
    })
# Similarly update case_update view
class CaseUpdateView(UpdateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/case_form.html'
    success_url = reverse_lazy('cases:case_list')

    def get_context_data(self, **kwargs):
        """Add document and hearing formsets to context."""
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['document_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['hearing_formset'] = HearingFormSet(self.request.POST, instance=self.object)
        else:
            context['document_formset'] = DocumentFormSet(instance=self.object)  # No need for explicit queryset
            context['hearing_formset'] = HearingFormSet(instance=self.object)

        return context


    def form_valid(self, form):
        context = self.get_context_data()
        document_formset = context['document_formset']
        hearing_formset = context['hearing_formset']

        if form.is_valid() and document_formset.is_valid() and hearing_formset.is_valid():
            self.object = form.save()

            # Set instance explicitly before saving formsets
            document_formset.instance = self.object
            document_formset.save()

            hearing_formset.instance = self.object
            hearing_formset.save()

            return super().form_valid(form)

        # If any formset is invalid, re-render the form with errors
        return self.render_to_response(self.get_context_data(form=form))



class CaseDeleteView(DeleteView):
    model = Case
    template_name = "cases/case_confirm_delete.html"
    success_url = reverse_lazy("cases:case_list")

class CaseCreateView(CreateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/case_form.html'
    success_url = reverse_lazy('cases:case_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['document_formset'] = DocumentFormSet(self.request.POST, self.request.FILES)
            context['hearing_formset'] = HearingFormSet(self.request.POST)
        else:
            context['document_formset'] = DocumentFormSet()
            context['hearing_formset'] = HearingFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        document_formset = context['document_formset']
        hearing_formset = context['hearing_formset']
        
        if document_formset.is_valid() and hearing_formset.is_valid():
            self.object = form.save()
            
            # Save documents
            document_formset.instance = self.object
            documents = document_formset.save()
            
            # Save hearings
            hearing_formset.instance = self.object
            hearings = hearing_formset.save()
            
            return super().form_valid(form)
        
        # If formsets are invalid, re-render with errors
        return self.render_to_response(self.get_context_data(form=form))
    