from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.views.generic import DetailView
from .models import Employee


class EmployeeDetailView(LoginRequiredMixin,SuperuserRequiredMixin,DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'