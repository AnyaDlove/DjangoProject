from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Employee


def home(request):
    return render(request, "employees/home.html")


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "employees/employee_list.html", {"employees": employees})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/employee_detail.html", {"employee": employee})
